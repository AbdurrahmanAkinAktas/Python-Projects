import cv2
import os
import numpy as np


faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,500);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,500);

id = input('Enter User ID: ')
sampleNo = input('Enter No. of Images ')
sampleNum = 0

directory = 'Users/user{}'.format(id)

print('creating Dataset')

if not os.path.exists(directory):
    os.makedirs(directory)

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        sampleNum+=1
        cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg', frame[y:y+h,x:x+w])
        cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
        cv2.waitKey(100)
    cv2.imshow('Face', frame)
    cv2.waitKey(1)
    if sampleNum > int(sampleNo):
        break

print('done')
cap.release()
cv2.destroyAllWindows()
