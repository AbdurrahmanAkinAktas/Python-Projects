import cv2
import numpy as np


faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

id = input('Enter User ID: ')
sampleNum = 0

print('creating Dataset')

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        sampleNum+=1
        cv2.imwrite('dataset/User.'+str(id)+'.'+str(sampleNum)+'.jpg', frame[y:y+h,x:x+w])
        cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
        cv2.waitKey(100)
    cv2.imshow('Face', frame)
    cv2.waitKey(1)
    if sampleNum > 100:
        break

cap.release()
cv2.destroyAllWindows()
