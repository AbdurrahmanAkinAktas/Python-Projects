import cv2
import os
import numpy as np
from PIL import Image
from PIL import ImageFile

print('Renaming the Files')
ImageFile.LOAD_TRUNCATED_IMAGES = True

recognizer = cv2.face.LBPHFaceRecognizer_create()
path='Users/user0'


def getImagesWithID(path):
    num = 1
    imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
##        print(imagePath, 'to', os.path.join(path, 'User.0.{}.jpg'.format(num)))
        os.rename(imagePath, path+'/'+str(num)+'.jpg')
        num+=1

getImagesWithID(path)
print('end')
