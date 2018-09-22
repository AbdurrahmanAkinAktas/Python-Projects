import cv2
import numpy as np
from tkinter import Tk
from tkinter import ttk


CONF_THRESHOLD= 55

faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainingData.xml')
id=0
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        id, conf = recognizer.predict(gray[y:y+h, x:x+w])
##        print(conf)
        if conf < CONF_THRESHOLD:
            if id == 0:
                id='Test User'
            elif id == 1:
                id='Akin'
            elif id == 2:
                id='Zumrut'
            else:
                id='Unknown'
        else:
            id='Not Confident Enough'
        cv2.putText(frame, str(id), (x,y+h), font, 1, (255,0,0), 3)      
    cv2.imshow('Face', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
