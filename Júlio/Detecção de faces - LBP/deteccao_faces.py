import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)
dst = cv2.imread("smile.jpg")

face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()

    src_mask = np.zeros(dst.shape, dst.dtype)
    poly = np.array([ [2,42], [4,28], [10,16], [20,8], [30,3], [41,1], [54,2], [66,4], [76, 11], [84,19], [89,28], [92,38], [92,48], [91,56], [88,62], [83,69], [78,74], [73,79], [64,83], [54,85], [42,45], [41,85], [33,83], [27,81], [22,78], [17,75], [11,70], [8,65], [4,59], [3,52] ], np.int32)
    cv2.fillPoly(src_mask, [poly], (255, 255, 255))

    cinza = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=1)
    img_c = frame.copy()
    for (x,y,w,h) in faces:
        center = (x,y)
        print(x,y, w,h)
        img_c = cv2.seamlessClone(dst, frame, src_mask, center, cv2.NORMAL_CLONE)
        
        
        
        cv2.rectangle(img_c,(x,y),(x+w,y+h),(255,0,0),2)
        # rdi: região de interesse
        #rdi = cinza[y:y+h, x:x+w]
        #rdi_cor = img_c[y:y+h, x:x+w]
        #olhos = eye_cascade.detectMultiScale(rdi)
        #for (ox,oy,ow,oh) in olhos:
        #    cv2.rectangle(rdi_cor,(ox,oy),(ox+ow,oy+oh),(0,255,0),2)
    #plt.imshow(img_c)
    cv2.imshow('Output', img_c)
    
    c = cv2.waitKey(1)
    if c == 10:
        break

cap.release()
cv2.destroyAllWindows()
