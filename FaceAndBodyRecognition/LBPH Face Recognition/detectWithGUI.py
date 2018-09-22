import cv2
import numpy as np
from tkinter import Tk
from tkinter import ttk
from tkinter import IntVar
from PIL import Image
from PIL import ImageTk
from PIL import ImageFile
import os
from datetime import datetime

WIDTH = 800
HEIGHT = 600
ttk_width = 20


master = Tk()
master.title('FaceAndBodyRecognition')
master.geometry('{}x{}'.format(WIDTH, HEIGHT))
gui = ttk.Frame(master)
gui.grid(row=0, column=1)

confidence_threshold = IntVar()
# Confidence level that is needed to determine the label of a face
confidence_threshold.set(55)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_detector = cv2.CascadeClassifier('haarcascade_fullbody_1.xml')

cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()

id = 0
font = cv2.FONT_HERSHEY_SIMPLEX

info_label = ttk.Label(master, text='Detecting and Recognizing Faces', foreground='orange',
                       background='black', padding=5, font=('Helvetica', 19, 'bold'), relief='ridge')
info_label.grid(row=1, column=0)

label_confidence_threshold = ttk.Label(
    gui, justify='center', text='Confidence Threshold:', width=ttk_width).grid(row=9, column=0)
entry_confidence_threshold = ttk.Entry(gui, justify='right', width=ttk_width)
entry_confidence_threshold.insert(0, '{}'.format(confidence_threshold.get()))
entry_confidence_threshold.grid(row=10, column=0)


def create_dataset(idp, img_num):
    id = idp
    sampleNum = 0
    print('creating Dataset')
    info_label.configure(text='Taking {} Pictures and Creating Dataset for User {}'.format(
        entry_img_num.get(), id))

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite('dataset/User.'+str(id)+'.' +
                        str(sampleNum)+'.jpg', gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), [255, 0, 0], 2)
            cv2.waitKey(100)
        cv2.waitKey(1)

        guiImg = Image.fromarray(frame)
        guiImg = ImageTk.PhotoImage(image=guiImg)
        stream.image = guiImg
        stream.configure(image=guiImg)

        master.update()

        if sampleNum > img_num:
            break


def delete_dataset(idp, img_num):
    id = idp
    print('deleting Dataset')
    info_label.configure(text='Deleting Dataset')

    try:
        while True:
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            for i in range(1, img_num+2):
                os.remove('dataset/User.'+str(id)+'.'+str(i)+'.jpg')
            cv2.waitKey(1)

            guiImg = Image.fromarray(frame)
            guiImg = ImageTk.PhotoImage(image=guiImg)
            stream.image = guiImg
            stream.configure(image=guiImg)

            master.update()
            break
    except:
        print('No Dataset to Delete')
        info_label.configure(text='No Dataset to Delete')


def train():
    global recognizer
    print('Training The Classifier')
    info_label.configure(text='Training the Recognizer')
    try:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        path = 'dataset'

        def getImagesWithID(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faces = []
            IDs = []
            for imagePath in imagePaths:
                faceImg = Image.open(imagePath).convert('L')
                cv2.waitKey(10)
                faceNp = np.array(faceImg, 'uint8')
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(faceNp)
                IDs.append(ID)
                cv2.imshow('training', faceNp)
                cv2.waitKey(10)
                master.update()
            return IDs, faces

        IDs, faces = getImagesWithID(path)
        recognizer.train(faces, np.array(IDs))
        recognizer.write('trainingData.xml')
        cv2.destroyAllWindows()
        master.update()
    except:
        print('No Dataset Available')
        info_label.configure(text='No Dataset Available')


def delete_recognizer():
    global recognizer
    print('deleting Recognizer')
    info_label.configure(text='Deleting Recognizer')

    blanks = []
    blankImg = Image.open('deletion/delete.0.jpg').convert('L')
    blankNp = np.array(blankImg, 'uint8')
    blanks.append(blankNp)
    blankImg = Image.open('deletion/delete.1.jpg').convert('L')
    blankNp = np.array(blankImg, 'uint8')
    blanks.append(blankNp)

    recognizer.train(blanks, np.array([0, 0]))


try:
    recognizer.read('trainingData.xml')
except:
    print('No trainingData.xml found')
    try:
        train()
    except:
        print('No Dataset found')
        create_dataset(0, 50)
        train()


stream = ttk.Label(master)
stream.grid(row=0, column=0)

label_user_id = ttk.Label(
    gui, justify='center', text='User ID:', width=ttk_width).grid(row=1, column=0)
entry_id = ttk.Entry(gui, justify='right', width=ttk_width)
entry_id.insert(0, '0')
entry_id.grid(row=2, column=0)

label_img_num = ttk.Label(
    gui, justify='center', text='Number of Images:', width=ttk_width).grid(row=3, column=0)
entry_img_num = ttk.Entry(gui, justify='right', width=ttk_width)
entry_img_num.insert(0, '100')
entry_img_num.grid(row=4, column=0)

button_create_dataset = ttk.Button(gui, text='Create Dataset', width=ttk_width, command=lambda: create_dataset(
    entry_id.get(), int(entry_img_num.get()))).grid(row=5, column=0)
button_train_recognizer = ttk.Button(
    gui, text='Train Recognizer', width=ttk_width, command=lambda: train()).grid(row=6, column=0)
button_delete_dataset = ttk.Button(gui, text='Delete Dataset', width=ttk_width, command=lambda: delete_dataset(
    entry_id.get(), int(entry_img_num.get()))).grid(row=7, column=0)
button_delete_recognizer = ttk.Button(
    gui, text='Delete Recognizer', width=ttk_width, command=lambda: delete_recognizer()).grid(row=8, column=0)


label_name = open('label_name.txt', 'r')
names = label_name.readlines()

label_names = ttk.Label(gui, relief='ridge', padding=5, text='ID:  User: \n{}   |  {}\n{}   |  {}\n{}   |  {}\n{}   |  {}\n{}   |  {}\n'.format(
    0, names[0][:-1], 1, names[1][:-1], 2, names[2][:-1], 3, names[3][:-1], 4, names[4][:-1])).grid(row=0, column=0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# scaleFactor -> smaller, more results, more expensive.
# minNeighbours -> higher value, less detection, higher quality
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
# size Akin at ~5m distance ~= 170 x 340 (body)
# expected size ~= 180 x 370 (body)      haarcascade_fullbody_1 is based on 32x64
    bodies = body_detector.detectMultiScale(gray, 1.2, 20, 0 | 1, (120, 240))

    try:
        confidence_threshold = entry_confidence_threshold.get()
    except:
        pass

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        if conf < float(confidence_threshold):
            if id == 0:
                id = '{}: {}'.format(names[0][:-1], round(conf))
            elif id == 1:
                id = '{}: {}'.format(names[1][:-1], round(conf))
            elif id == 2:
                id = '{}: {}'.format(names[2][:-1], round(conf))
            elif id == 3:
                id = '{}: {}'.format(names[3][:-1], round(conf))
            elif id == 4:
                id = '{}: {}'.format(names[4][:-1], round(conf))
            cv2.putText(frame, str(id), (x, y+h), font, 1, (255, 0, 0), 3)
        else:
            id = 'Not Confident Enough: {}'.format(round(conf))
            cv2.putText(frame, str(id), (x, y+h), font, 0.8, (255, 0, 0), 3)

    for (x, y, w, h) in bodies:
        # print(x,y,w,h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    try:
        guiImg = Image.fromarray(frame)
        guiImg = ImageTk.PhotoImage(image=guiImg)
        stream.image = guiImg
        stream.configure(image=guiImg)
        info_label.configure(text='Detecting and Recognizing Faces')
        master.update()
    except:
        print('no frame to show, exiting')
        break


print('releasing and closing')
cap.release()
cv2.destroyAllWindows()
label_name.close()


master.mainloop()
