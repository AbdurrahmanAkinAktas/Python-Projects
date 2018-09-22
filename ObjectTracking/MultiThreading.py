import threading
import time
import cv2
print_lock=threading.Lock()


##def test1():
##    while True:
##        with print_lock:
##            print('hi')
##        time.sleep(0.2)

def test1():
    cap = cv2.VideoCapture(0)
    while True:
        print('working')
        ret, frame = cap.read()
        cv2.imshow('test', frame)
##        with frame_buffer_lock:
##            frame_buffer = frame
        key = cv2.waitKey(0) & 0xFF
        if key == 27:
         break

def test2():
    while True:
        with print_lock:
            print('bye')
        time.sleep(0.2)


##t1=threading.Thread(target=test1, daemon=True)
##t2=threading.Thread(target=test2, daemon=True)
##
##t1.start()
##t2.start()
##
##t1.join()
##t2.join()




cap = cv2.VideoCapture(0)
while True:
    print('producing')
    ret, frame = cap.read()
    cv2.imshow('test', frame)
    cv2.waitKey(1)













        
