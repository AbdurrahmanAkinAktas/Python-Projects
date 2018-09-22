import cv2
import numpy as np
import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

akin = cv2.imread('akin0.jpg', 0)
icetea = cv2.imread('icetea0.jpg', 0)

w, h = akin.shape[::-1]
w2, h2 = icetea.shape[::-1]

threshold = 0.75

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)

    result = cv2.matchTemplate(equalized, akin, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    result2 = cv2.matchTemplate(equalized, icetea, cv2.TM_CCOEFF_NORMED)

    loc2 = np.where(result2 >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (255,0,0), 2)

    for pt in zip(*loc2[::-1]):
        cv2.rectangle(frame, pt, (pt[0]+w2, pt[1]+h2), (0,0,255), 2)
 
    cv2.imshow('Face and Body Detection', frame)

    key = cv2.waitKey(10) & 0xFF
    if key == 27:
         break

cap.release()
cv2.destroyAllWindows()
    
