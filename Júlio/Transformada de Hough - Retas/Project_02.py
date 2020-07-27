import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    
    cv2.imshow('Input', frame)
    bordas = cv2.Canny(frame, 50, 200)
    cv2.imshow('Bordas', bordas)

    linhas_P = cv2.HoughLinesP(bordas, 1, np.pi / 180, 10, minLineLength=100, maxLineGap=100)
    bordas_copia = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
    for linha in linhas_P:
        x1, y1, x2, y2 = linha[0]
        cv2.line(bordas_copia, (x1, y1), (x2, y2), (0, 0, 255), 3)
    
    cv2.imshow('Bordas cópia', bordas_copia)
    
    c = cv2.waitKey(1)
    if c == 10:
        break

cap.release()
cv2.destroyAllWindows()