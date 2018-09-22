import cv2
import numpy as np
import sys

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
##body_detector = cv2.CascadeClassifier('haarcascade_fullbody.xml')

tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

multi_tracker = cv2.MultiTracker_create()

#get camera feed
cap = cv2.VideoCapture(0)

# Exit if video not opened.
if not cap.isOpened():
    print ('Could not open video')
    sys.exit()

#get first frame to define object
ok, frame = cap.read()
#if reading from a file fails
if not ok:
    print ('Cannot read video')
    sys.exit()

#convert image to grayscale
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

#detect objects
faces = face_detector.detectMultiScale(gray, 1.3, 5)
##bodies = body_detector.detectMultiScale(gray, 1.3, 5)

#define ROI bounding boxes and add to the tracker list
old_box = []
bounding_boxes=[]
for (x,y,w,h) in faces:
    cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
    bounding_boxes.append((x,y,w,h))

#Initialize trackers with first frame and bounding box
for bbox in bounding_boxes:
    if tracker_type == 'BOOSTING':
        ok = multi_tracker.add(cv2.TrackerBoosting_create(), frame, bbox)
    if tracker_type == 'MIL':
        ok = multi_tracker.add(cv2.TrackerMIL_create(), frame, bbox)
    if tracker_type == 'KCF':
        ok = multi_tracker.add(cv2.TrackerKCF_create(), frame, bbox)
    if tracker_type == 'TLD':
        ok = multi_tracker.add(cv2.TrackerTLD_create(), frame, bbox)
    if tracker_type == 'MEDIANFLOW':
        ok = multi_tracker.add(cv2.TrackerMedianFlow_create(), frame, bbox)
    if tracker_type == 'GOTURN':
        ok = multi_tracker.add(cv2.TrackerGOTURN_create(), frame, bbox)

#update tracker with every frame
lost = False
while True:
    ok, frame = cap.read()
    if not ok:
        break

##    if lost:
##        print('lost someone')

    #start timer
    timer = cv2.getTickCount()

    old_box = bounding_boxes
    #update trackers
    ok, bounding_boxes = multi_tracker.update(frame)
    
    #calculate FPS
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    

    #draw bounding box around the object
    if ok:
        for i in range(0, len(bounding_boxes)):
            point1 = int(bounding_boxes[i][0]) , int(bounding_boxes[i][1])
            point2 = int(bounding_boxes[i][0] + bounding_boxes[i][2]), int(bounding_boxes[i][1] + bounding_boxes[i][3])
            cv2.rectangle(frame,point1, point2,[255,0,0],2)
            cv2.putText(frame, str(i), (int(bounding_boxes[i][0]) , int(bounding_boxes[i][1]+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
##    else:
##        for bounding_box in bounding_boxes:
##            point1 = int(bounding_box[0]) , int(bounding_box[1])
##            point2 = int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3])
##            cv2.rectangle(frame,point1, point2,[0,0,255],2)
##            cv2.putText(frame, "Last Known Location", (int(bounding_box[0]) , int(bounding_box[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        #tracking failed, at least one object was lost
        cv2.putText(frame, "Tracking Failure", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        lost = True
    # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
 
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    #Display final image
    cv2.imshow("ObjectTracking", frame)
    
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        cap.release()
        cv2.destroyAllWindows()
        break




























