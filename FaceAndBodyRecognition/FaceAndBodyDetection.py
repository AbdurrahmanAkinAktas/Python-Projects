import cv2
import numpy as np
import datetime


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(equalized, 1.2, 5)
    profiles = profile_cascade.detectMultiScale(equalized, 1.2, 5)
    bodies = body_cascade.detectMultiScale(equalized, 1.1, 3)

    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
##        print("Face Found {}".format(datetime.datetime.now()))

    for (x,y,w,h) in profiles:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

    for (x,y,w,h) in bodies:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
##        print("Body Found {}".format(datetime.datetime.now()))
 
    cv2.imshow('Face and Body Detection', frame)

    key = cv2.waitKey(10) & 0xFF
    if key == 27:
         break

cap.release()
cv2.destroyAllWindows()
    
