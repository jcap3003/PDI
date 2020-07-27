import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()

    cinza = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(cinza, scaleFactor=2, minNeighbors=1)
    img_c = frame.copy()
    for (x,y,w,h) in faces:
        cv2.rectangle(img_c,(x,y),(x+w,y+h),(255,0,0),2)
        # rdi: região de interesse
        rdi = cinza[y:y+h, x:x+w]
        rdi_cor = img_c[y:y+h, x:x+w]
        olhos = eye_cascade.detectMultiScale(rdi)
        for (ox,oy,ow,oh) in olhos:
            cv2.rectangle(rdi_cor,(ox,oy),(ox+ow,oy+oh),(0,255,0),2)
    #plt.imshow(img_c)
    cv2.imshow('Output', img_c)
    
    c = cv2.waitKey(1)
    if c == 10:
        break

cap.release()
cv2.destroyAllWindows()
