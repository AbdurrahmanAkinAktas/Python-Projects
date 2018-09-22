import cv2
import numpy as np


faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print('cutting out faces')

num = 1
spacer = '000'
while True:
    try:
        print('dataset4/image_'+spacer+str(num)+'.jpg')
        frame = cv2.imread('dataset4/image_'+spacer+str(num)+'.jpg',0) #load as grayscale
        num+=1
        if num is 10:
            spacer = '00'
        elif num is 100:
            spacer = '0'
            
        faces = faceDetector.detectMultiScale(frame,1.3,5)
        cv2.imshow('Face', frame)

        for (x,y,w,h) in faces:
            cv2.imwrite('dataset5/User.'+str(0)+'.'+str(num)+'.jpg', frame[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
            cv2.waitKey(1)
        cv2.imshow('Face', frame)
        cv2.waitKey(1)

        
    except Exception as e:
        print('no faces', e)
        continue

cv2.destroyAllWindows()
