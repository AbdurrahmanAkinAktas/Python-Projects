import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import IntVar
from tkinter import Tk
from tkinter import ttk

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


WIDTH = 1300
HEIGHT = 600

master = Tk()
master.title('VideoReplay')
master.geometry('{}x{}'.format(WIDTH, HEIGHT))
gui = ttk.Frame(master)
gui.pack(side='bottom', fill='both')

oldFrameNo = IntVar()
frameNo = IntVar()
frameNo.set(1)
oldFrameNo.set(frameNo.get())

out = None

stream = ttk.Label(master)
stream.pack(side="top")
currentAction = 'stop'
currentSnapshot = None

def getFrame(video):
        global currentSnapshot
        ret, currentFrame = video.read()
        currentFrame = cv2.resize(currentFrame, (1280,720))
        #out.write(currentFrame)
      ##  faces = face_cascade.detectMultiScale(currentFrame, 1.3, 5)

      #  for (x,y,w,h) in faces:
       #         cv2.rectangle(currentFrame, (x,y), (x+w, y+h), (0,255,0), 2)
                
        final = Image.fromarray(currentFrame)
        currentSnapshot = Image.fromarray(currentFrame)
        final = ImageTk.PhotoImage(image = final)
        oldFrameNo.set(frameNo.get())
        frameNo.set(frameNo.get()+1)
        return final

def displayVideo(video, videoPath):
        global currentAction
        global out
        firstFrame = True
        snapshotNo = 0

        while True:
                if currentAction is 'play':
                        final = getFrame(video)
                        stream.configure(image=final)
                        stream.image = final

                elif currentAction is 'stop':
                        if firstFrame:
                                final = getFrame(video)
                                stream.configure(image=final)
                                stream.image = final
                                firstFrame = False

                elif currentAction is 'frame':
                        final = getFrame(video)
                        stream.configure(image=final)
                        stream.image = final
                        currentAction = 'stop'
        
                elif currentAction is 'goToFrame':

#                         Manual way of jumping to a frame
#                        
##                        video = cv2.VideoCapture(videoPath)
##                        frameNo.set(int(EntryFrameNo.get()))
##                        for i in range(frameNo.get()):
##                                ret, currentFrame = video.read()


                        if frameNo.get() <= video.get(cv2.CAP_PROP_FRAME_COUNT):
                                oldFrameNo.set(frameNo.get())
                                frameNo.set(frameNo.get()-1)
                                video.set(cv2.CAP_PROP_POS_FRAMES, frameNo.get()-1)
                                final = getFrame(video)
                                stream.configure(image=final)
                                stream.image = final
                        else:
                                frameNo.set(oldFrameNo.get() + 1)
                                
                        currentAction = 'stop'


                elif currentAction is 'saveFrame':
                        if currentSnapshot is not None:
                                currentSnapshot.save('snapshot{}.jpg'.format(snapshotNo))
                                snapshotNo+=1
                                currentAction = 'stop'
                        
                        
                master.update()


            

def getVideo():
        global out
        videoPath = EntryVideoPath.get()
        try:

##                To use a video file
                video = cv2.VideoCapture(videoPath)


##              To use a webcam
##                video = cv2.VideoCapture(0)
                
                #if you want to save the video to a new file with 50 fps
                #fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
                #out = cv2.VideoWriter('out.mkv', fourcc,50.0, (1280,720))
                displayVideo(video, videoPath)
                print("got video and set play true")
        except cv2.error as e:
                print('No such file found!', e)
        
def play():
        global currentAction
        currentAction = 'play'
        print("now playing")

def stop():
        global currentAction
        currentAction = 'stop'
        print("now stopping")

def nextFrame():
        global currentAction
        currentAction = 'frame'
        print("now getting frame")

def goToFrame():
        global currentAction
        currentAction = 'goToFrame'
        print('going to frame', frameNo)

def saveFrame():
        global currentAction
        currentAction = 'saveFrame'
        print("saving frame")

        
EntryVideoPath = ttk.Entry(gui, text = 'test', width = 50)
EntryVideoPath.grid(row=0, column=0)



ButtonGetVideo = ttk.Button(gui, text = 'Get Video', command = getVideo).grid(row=0, column=1)
ButtonPlay = ttk.Button(gui, text = 'Play', command = play).grid(row=0, column=2)
ButtonStop = ttk.Button(gui, text = 'Stop', command = stop).grid(row=0, column=3)
ButtonNextFrame = ttk.Button(gui, text = 'Next Frame', command = nextFrame).grid(row=0, column=4)

EntryFrameNo = ttk.Entry(gui, width = 15, justify = 'right', text=frameNo)
EntryFrameNo.grid(row=0, column=5)

ButtonGoToFrame = ttk.Button(gui, text = 'Go To Frame', command = goToFrame).grid(row=0, column=6)

ButtonSaveFrame = ttk.Button(gui, text = 'Save Frame', command = saveFrame).grid(row=0, column=7)
        
master.mainloop()
