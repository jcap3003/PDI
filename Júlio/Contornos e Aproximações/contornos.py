import cv2
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy

cap = cv2.VideoCapture(0)
dst = cv2.imread("paisagem.jpg")

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()

    #src_mask = np.zeros(frame.shape, frame.dtype)
    src_mask = np.zeros(dst.shape, dst.dtype)
    poly = np.array([ [203,478], [236,386], [265,351], [288,198], [344,125], [411,197], [433,326], [442,343], [470, 352], [520,474] ], np.int32)
    #poly = np.array([ [0,0], [639,0], [639,479], [0,479] ], np.int32)
    cv2.fillPoly(src_mask, [poly], (255, 255, 255))
    
    # This is where the CENTER of the airplane will be placed
    center = (300,302)
 
    # Clone seamlessly.
    output = cv2.seamlessClone(dst, frame, src_mask, center, cv2.NORMAL_CLONE)
 
    # Save result
    #cv2.imwrite("images/opencv-seamless-cloning-example.jpg", output);
    cv2.imshow('Output', output)
    
    c = cv2.waitKey(1)
    if c == 10:
        break

cap.release()
cv2.destroyAllWindows()
