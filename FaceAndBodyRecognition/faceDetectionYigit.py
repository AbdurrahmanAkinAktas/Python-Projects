# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 00:10:40 2017

@author: alp
"""

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

profil_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture(0);

#img = cv2.resize(img,(1000,1000),interpolation = cv2.INTER_CUBIC)

while True:
    ret,frame = cap.read()
    #frame = cv2.imread("h.jpg")  
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray,1.1,4)

    bodies = body_cascade.detectMultiScale(gray,1.3,5)

    profil_faces = profil_face_cascade.detectMultiScale(gray,1.3,5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
        roi = frame[y:y+h,x:x+w]
        
    for (x,y,w,h) in bodies:
        cv2.rectangle(frame,(x,y),(x+w,y+h),[0,255,0],2)
    
    for (x,y,w,h) in profil_faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),[0,0,255],2)
   
    #cv2.imshow('test22222',roi_color)
    cv2.imshow('test',frame)
    #cv2.imwrite('ben.png',roi_color)
    if(cv2.waitKey(1) & 0xFF==ord('q')):
            break
cap.release() 
cv2.destroyAllWindows()



