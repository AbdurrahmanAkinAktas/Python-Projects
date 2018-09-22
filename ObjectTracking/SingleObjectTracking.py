import cv2
import numpy as np
import sys

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
##body_detector = cv2.CascadeClassifier('haarcascade_fullbody.xml')

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting_create()
if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD_create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow_create()
if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN_create()

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

#define ROI bounding boxes
for (x,y,w,h) in faces:
    cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
    bounding_box=(x,y,w,h)

#Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bounding_box)

#update tracker with every frame
while True:
    ok, frame = cap.read()
    if not ok:
        break

    #start timer
    timer = cv2.getTickCount()

    old_bb = bounding_box

    #update tracker
    ok, bounding_box = tracker.update(frame)

    print('old: ', old_bb, 'new: ', bounding_box)
    #calculate FPS
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    #draw bounding box around the object
    if ok:
        point1 = int(bounding_box[0]) , int(bounding_box[1])
        point2 = int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3])
        cv2.rectangle(frame,point1, point2,[255,0,0],2)
    else:
        #tracking failed, lost object
        cv2.putText(frame, "Tracking Failure", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

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




























