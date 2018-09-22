import cv2
import numpy as np
import matplotlib.pyplot as plt

akin = cv2.imread('sample0.png', 0)
icetea = cv2.imread('icetea0.jpg', 0)

akin2 = cv2.imread('sample1.png', 0)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(akin, None)
kp2, des2 = orb.detectAndCompute(akin2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

result = cv2.drawMatches(akin, kp1, akin2, kp2, matches[:20], None, flags=2)

plt.imshow(result)
plt.show()

##cap = cv2.VideoCapture(0)
##
##while True:
##    ret, frame = cap.read()
##    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
####    equalized = cv2.equalizeHist(gray)
##
##    kp2, des2 = orb.detectAndCompute(frame, None)
##
##    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
##
##    matches = bf.match(des1, des2)
##    matches = sorted(matches, key = lambda x:x.distance)
##
##    result = cv2.drawMatches(akin, kp1, frame, kp2, matches[:20], None, flags=2)
##
##    plt.imshow(result)
##    plt.show()


##    cv2.imshow('Feature Matching', frame)

key = cv2.waitKey(10) & 0xFF
##if key == 27:
##    break

cap.release()
cv2.destroyAllWindows()
    

