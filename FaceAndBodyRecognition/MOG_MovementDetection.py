import cv2
import numpy as np

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()



##
##          MOG2 -> filtering -> contours -> 2second degree contours which 
##              pass filtering by weight



while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
   

    kernel = np.ones((4,4), np.uint8)

    opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

##    cv2.imshow('original', frame)
##    cv2.imshow('fg', fgmask)
##    cv2.imshow('opening', opening)

    open_dilation = cv2.dilate(opening, kernel, iterations=1)
    open_erosion = cv2.erode(opening, kernel, iterations=1)
    
    final = cv2.bitwise_and(frame, frame, mask=fgmask)
    final2 = cv2.bitwise_and(frame, frame, mask=open_dilation)
    final3 = cv2.bitwise_and(frame, frame, mask=open_erosion)

    cv2.imshow('opening',final)
    cv2.imshow('open_dilation',final2)
    cv2.imshow('open_erosion',final3)


    key = cv2.waitKey(10) & 0xFF
    if key == 27:
         break

cap.release()
cv2.destroyAllWindows()
    
