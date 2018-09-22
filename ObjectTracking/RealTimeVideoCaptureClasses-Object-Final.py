import numpy as np
import threading
import train
import time
import sys
import cv2
import os

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
##body_detector = cv2.CascadeClassifier('haarcascade_fullbody.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

if not os.path.exists('trainingData.xml'):
    print('initial training of the recognizer')
    train.train()
    
recognizer.read('trainingData.xml')
recognizer_lock = threading.Lock()

exit = False
show_final = True #confirm that the curretn frame was updated as needed by all classes

print_lock = threading.Lock()
frame_buffer_lock = threading.Lock()
detected_faces_lock = threading.Lock()
##detected_bodies_lock = threading.Lock()

detect_event = threading.Event()
detect_event.set()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,700);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,700);
frame_buffer = None

detected_faces=[]#the bounding boxes of the found faces
##detected_bodies=[]#the bounding boxes of the found bodies

labels = open('Users/labels.txt', 'r')
names = labels.read().split(',')[:-1]
labels.close()

people = []

class person:
    def __init__(self, bbox):
        self.tracker = cv2.TrackerKCF_create()
        with frame_buffer_lock:
            self.tracker.init(frame_buffer, bbox)

        self.ok = True  #is tracker still tracking
        
        self.bbox = bbox
        self.bbox_lock = threading.Lock()
        self.detected_bbox = None
        self.old_bbox = self.bbox   #1 frame old bbox

        self.scanned = False

        self.recovering = False #was lost and is being recovered
        
        self.id = 0  #id after identified as a known (or unknown) person
        self.id_final = False #True when the id was confirmed with high enough accuracy
        self.new_id_confirmed = False #if the confidence is below the threshold, but the face is still unknown
        self.id_lock = threading.Lock()

        self.conf = 1000  #just so it is disregarded
        

    def to_string(self):
        print('Tracker: ', self.tracker, '\nok: ', self.ok, '\nbbox: ', self.bbox,
              '\nold_bbox: ', self.old_bbox, '\ndetected_bbox: ', self.detected_bbox,'\nscanned: ', self.scanned,
              '\nid: ' , self.id,'|', names[self.id],'confidence: ', self.conf, '\nid_final: ', self.id_final, '\nrecovering: ', self.recovering, '\n----------------------')


    def lost(self):
##        print('new recoverer thread started for {}'.format(self.id))
        time.sleep(0.7)
        gray = cv2.cvtColor(get_frame(), cv2.COLOR_BGR2GRAY)
        gray = gray[int(self.old_bbox[1]*0.9):int((self.old_bbox[1]+self.old_bbox[3])*1.1),
                    int(self.old_bbox[0]*0.9):int((self.old_bbox[0]+self.old_bbox[2])*1.1)]
        with detected_faces_lock:
            found = face_detector.detectMultiScale(gray, 1.3, 5)

            if len(found) > 0:
                self.tracker.init(get_frame(), (found[0][0],found[0][1],found[0][2],found[0][3]))
                self.ok=True
                self.recovering = False
            else:
    ##            print('tracker could not be recovered for {}, deleting person'.format(self.id))
                del(people[people.index(self)])               
            
            
    def save_new_id(self):
        self.to_string()
        directory = 'Users/user{}'.format(self.id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        num = 1
        for i in range(30):
            cv2.imwrite(directory+'/'+str(num)+'.jpg', get_frame()[int(self.detected_bbox[1]):int(self.detected_bbox[1]+self.detected_bbox[3]),
                int(self.detected_bbox[0]):int(self.detected_bbox[0]+self.detected_bbox[2])])
            print('took picture', i)
            num+=1
            cv2.waitKey(50)
        train.train()
        with recognizer_lock:
            recognizer.read('trainingData.xml')

    def update_tracker(self):
        if self.ok:
            with self.bbox_lock:
                self.old_bbox = self.bbox
                with frame_buffer_lock:
                    self.ok, self.bbox = self.tracker.update(frame_buffer)
                    if (self.ok) and (self.scanned) and (abs(self.bbox[2] - self.detected_bbox[2]) > self.detected_bbox[2]*0.1):
                        self.scanned = False
                        self.bbox = self.detected_bbox
                        self.tracker = cv2.TrackerKCF_create()
                        self.tracker.init(frame_buffer, self.bbox)
        else:
            if not self.recovering:
                self.recovering = True
                recover = threading.Thread(target= lambda : self.lost(), name='Recoverer for {}'.format(self.id), daemon = True)
                recover.start()

        if self.new_id_confirmed:
            self.new_id_confirmed = False
            t_new_id = threading.Thread(target = lambda : self.save_new_id(),name = 'saving new id for {}: {}'.format(self.id, self.conf), daemon = True ) 
            t_new_id.start()
    
    
def get_frame():
    with frame_buffer_lock:
        return frame_buffer


class producer(threading.Thread):
    
    def __init__(self,name, daemon):
        threading.Thread.__init__(self)
        self.daemon=daemon
        self.name = name

    def run(self):
        global frame_buffer
        
        while not exit:
            timer = cv2.getTickCount() #start fps timer
            ret, frame = cap.read()
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer) #calculate fps
##            print('Producer FPS: ', fps)
##            cv2.putText(frame, "Producer FPS : " + str(int(fps)), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 1);

            with frame_buffer_lock:
                frame_buffer = frame
                
            cv2.waitKey(1)


class detector(threading.Thread):
    
    def __init__(self,name, daemon):
        threading.Thread.__init__(self)
        self.daemon=daemon
        self.name = name

        self.MARGIN = 100 #max pixel diff for same face
        self.CONF_THRESHOLD_INSECURE = 130      #anything with more than this will be unknown no matter what
        self.CONF_THRESHOLD_UNKNOWN = 60        #anything better than this for otherface will be added to the known list
        self.CONF_THRESHOLD_KNOWN = 55          #anything better than this for a known face will be marked as id_final

    def detect(self):
        global detected_faces
        global frame_buffer
        global names

        if not exit:           
            gray = cv2.cvtColor(get_frame(), cv2.COLOR_BGR2GRAY)
            with detected_faces_lock: #and detected_bodies_lock:
    ##            detected_faces = new_faces
    ##            detected_bodies = body_detector.detectMultiScale(get_frame(), 1.3, 5)
                detected_faces = face_detector.detectMultiScale(gray, 1.3, 5)

                if True:    #len(detected_faces) > len(people):
                    for (x,y,w,h) in detected_faces:
##                        print('face found')
                        new_face = True
                        for p in people:
                            with p.bbox_lock:
                                if abs(p.bbox[0] - x) <= self.MARGIN or abs(p.bbox[1] - y) <= self.MARGIN:
##                                    print('not a new face, skipping')
                                    new_face = False
                                    p.detected_bbox = (x,y,w,h)
                                    p.scanned = True
                                    break
                                else:
                                    continue
##                                    print('not matching any other face until now')

                        if new_face:
##                            print('no match was found for this face, creating new person')
                            new_person = person((x,y,w,h))
                            new_person.detected_bbox = (x,y,w,h)
                            people.append(new_person)

    def identify(self):
        if not exit: 
            for p in people:
                if p.ok:
                    with p.id_lock:
                        if p.id_final:  #the id is confirmed already
##                            print('id already confirmed as {}'.format(p.id))
                            continue
                        else:
##                            print('id not yet confirmed')
                            gray = cv2.cvtColor(get_frame(), cv2.COLOR_BGR2GRAY)
                            with recognizer_lock:
                                id, conf = recognizer.predict(gray[int(p.detected_bbox[1]):int(p.detected_bbox[1]+p.detected_bbox[3]),
                                                               int(p.detected_bbox[0]):int(p.detected_bbox[0]+p.detected_bbox[2])])
##                            print('recognized as', id)
                            pid=0
                            #if too unconfident
                            if conf >= self.CONF_THRESHOLD_INSECURE:
                                pid = -1
##                                print('in insecure', id)
                            #confident that it is a person yet unknown
                            else:
                                if id == 0:
                                    if conf < self.CONF_THRESHOLD_UNKNOWN:
                                        #add to known list, id_final, create new id
                                        new_name = 'User{}'.format(len(names))
                                        names.append(new_name)
                                        with open('Users/labels.txt', 'a') as labels:
                                            labels.write(new_name+',')
                                        p.id_final = True
                                        p.new_id_confirmed = True
                                        pid=len(names)-1
                                else:
                                    pid=id
                            p.id = pid
                            p.conf = conf

                    #confident it is a person already known
                    if conf < self.CONF_THRESHOLD_KNOWN and (id != 0): #thus, no one will be saved as otherface. only known people will get id_final = True
                        p.id_final = True
                       
    def run(self):
        global relevant_detect
        time.sleep(2)
        while not exit:
                detect_event.wait(2)    #timer before re-detect if no event occurs
                self.detect()
                self.identify()
                relevant_detect = True
                detect_event.clear()

class tracker(threading.Thread):
    
    def __init__(self,name, daemon):
        threading.Thread.__init__(self)
        self.daemon=daemon
        self.name = name
        self.daemon = daemon
        
    def run(self):
        global frame_buffer
        global show_final

        #initial delay
        time.sleep(3)

        #main loop for this thread
        while not exit:

            #start timer for fps calculation
            timer = cv2.getTickCount()
            
            #if no trackers exist, skip
            if len(people) is 0:
                show_final = True
                continue

            #update trackers
            for p in people:
                p.update_tracker()

            #draw rectangles for trackers
            for p in people:
                with p.bbox_lock:
                    if p.ok:
                        point1 = int(p.bbox[0]) , int(p.bbox[1])
                        point2 = int(p.bbox[0] + p.bbox[2]), int(p.bbox[1] + p.bbox[3])
                        with p.id_lock:
                                if p.id == -1 or p.id > len(names):
                                    name = 'insecure'
                                else:
                                    name = names[p.id]
                                if not p.id_final:
                                    name += (': ' + str(round(p.conf)))
                                    
                        with frame_buffer_lock:
                            cv2.rectangle(frame_buffer,point1, point2,[255,0,0],2)
                            cv2.putText(frame_buffer, name, (int(p.bbox[0]), int(p.bbox[1]-20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)    

            #calculate and print fps
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            with frame_buffer_lock:            
                cv2.putText(frame_buffer, "Tracker FPS : " + str(int(fps)), (20,25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,70,50), 1)

            show_final = True
            
def show():
    time.sleep(2)
    global exit
    global show_final
    
    while not exit:
        if show_final:
            show_final = False
            cv2.imshow('frame buffer', get_frame())
            
            k = cv2.waitKey(1)
            if k == 27:
                exit = True
                cap.release()
                cv2.destroyAllWindows()
##                label_name.close()
                time.sleep(1)
##                sys.exit()
                break

t_producer = producer('Producer Thread', True) #producer thread
t_detector = detector('Detector Thread', True) #detector thread
t_show = threading.Thread(target=show, daemon=True, name='Displaying Thread') #show thread
t_track = tracker('Tracker Thread', True) #tracker thread

t_producer.start()
t_detector.start()
t_show.start()
t_track.start()






















