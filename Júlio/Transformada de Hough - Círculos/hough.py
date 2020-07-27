import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    
    #cv2.imshow('Input', frame)
    bordas = cv2.Canny(frame, 50, 200)
    #cv2.imshow('Bordas', bordas)
    #h1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    circulos = cv2.HoughCircles(bordas, cv2.HOUGH_GRADIENT, dp=1.02, minDist=200)
    
    if circulos is not None:
        circulos = np.round(circulos[0, :]).astype("int")

        for circulo in circulos:
            cv2.circle(frame, (circulo[0], circulo[1]), circulo[2], (255, 0, 0), 4)
    
    #plt.imshow(h1)
    cv2.imshow('Circulos', frame)
    
    c = cv2.waitKey(1)
    if c == 10:
        break

cap.release()
cv2.destroyAllWindows()