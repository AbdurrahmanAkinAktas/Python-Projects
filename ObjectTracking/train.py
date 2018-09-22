import cv2
import os
import numpy as np
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

recognizer = cv2.face.LBPHFaceRecognizer_create()
faces=[]
IDs=[]
def getImagesWithID():
    faces=[]
    IDs=[]
    for file in os.listdir('Users/'):
        if file[:4] == 'user':
            ID=int(file[4:])
            for img in os.listdir('Users/'+file):
                faceImg=Image.open('Users/'+file+'/'+img).convert('L')
##                cv2.waitKey(1)
                faceNp=np.array(faceImg, 'uint8')
                faces.append(faceNp)
                IDs.append(ID)
##                cv2.imshow('training', faceNp)
                cv2.waitKey(1)
    return IDs, faces
               
def train():
    IDs ,faces = getImagesWithID()
    print('Training the Classifier')
    recognizer.train(faces, np.array(IDs))
    print('Saving the Classifier')
    recognizer.write('trainingData.xml')
    print('Done')
    cv2.destroyAllWindows()

if __name__ == '__main__':
    train()
