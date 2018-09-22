import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
##  est color filter range to orange 
    mask = cv2.inRange(hsv, np.array([0,100,100]), np.array([30,255,255]))
    res = cv2.bitwise_and(hsv, hsv, mask=mask)


    cv2.imshow('Contour Object Tracking', res)
    

    key = cv2.waitKey(10) & 0xFF
    if key == 27:
         break

cap.release()
cv2.destroyAllWindows()
