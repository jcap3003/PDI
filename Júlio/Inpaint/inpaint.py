#%matplotlib inline
import cv2 # OpenCV
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

img = plt.imread('image.jpg')
mascara = cv2.imread('Mask.jpg', 0)

inpainted = cv2.inpaint(img, mascara, 3, cv2.INPAINT_TELEA)
while True:
    inpainted = cv2.inpaint(img, mascara, 3, cv2.INPAINT_TELEA)
    cv.imshow('Inpaint Output using NS Technique', inpainted)