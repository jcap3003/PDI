import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)
peppa = plt.imread('peppa.jpg',1)
#rows, cols = cap.shape[:2]

pts1 = np.float32([[723,160],[834,161],[714,273],[836,276]])
pts2 = np.float32([[0,0],[639,0],[0,479],[639,479]])
M = cv2.getPerspectiveTransform(pts2,pts1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    
    #frame = cv2.resize(frame, None, fx=0.20, fy=0.24, interpolation=cv2.INTER_AREA)
    pers = cv2.warpPerspective(frame, M, (peppa.shape[1],peppa.shape[0]), peppa, borderMode=cv2.BORDER_TRANSPARENT)
    cv2.imshow('Input', frame)
    cv2.imshow('peppa', pers)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()