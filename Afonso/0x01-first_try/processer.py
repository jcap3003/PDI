import cv2
import numpy as np
#from skimage.util import random_noise, img_as_ubyte
from keras.applications import imagenet_utils

def processer(frame, frame_number, model, preprocess):
    frame = gray_converter(frame)
    
    pyrd1 = cv2.pyrDown(frame)
    
    pyrd2 = cv2.pyrDown(pyrd1)
   
    pyru1 = cv2.pyrUp(frame)
    pyru2 = cv2.pyrUp(pyru1)
    add_hist(frame)
    add_hist(pyrd1)
    add_hist(pyrd2)
    add_hist(pyru1)
    add_hist(pyru2)
    cv2.putText(pyrd1,'d1', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(pyrd2,'d2', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(pyru1,'u1', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(pyru2,'u2', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.imshow('pyrd1',pyrd1)
    cv2.imshow('pyrd2',pyrd2)
    cv2.imshow('pyru1',pyru1)
    cv2.imshow('pyru2',pyru2)
    #do the processing
    #processed = gray_converter(frame)
    #processed = cv2.bilateralFilter(processed,9,100,100)
    #processed = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #cv2.imshow('framer',processed)
    #processed = do_the_learning(processed, model, preprocess)
    #processed = cv2.cvtColor(processed, cv2.COLOR_RGB2BGR)
    cv2.putText(frame,'PROCESSED IMAGE', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.imshow('frame',frame)


def add_hist(img):
    h = cv2.calcHist([img],[0],None,[256],[0,256])
    for i, bin_ in enumerate(h):
        cv2.line(img,(i,img.shape[0]),(i,img.shape[0] - int(bin_*10/img.shape[0])),(255,255,255))
    cv2.line(img,(257,img.shape[0]),(257,img.shape[0] - 50),(0,255,255))
    return h.reshape((-1)).T

def filter_img(img,kernel = np.ones((3, 3), dtype="float32")/9):
    return cv2.filter2D(img, -1, kernel)
def gray_converter(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def noise_cleaning(processed):
    processed = random_noise(processed, mode='s&p')
    #processed*=255
    #processed = processed.astype(int)
    left, right = processed[:,:processed.shape[1]//2] , processed[:,processed.shape[1]//2:]
    #right = cv2.medianBlur(np.float32(right), 3)
    left = cv2.medianBlur(np.float32(left), 3)
    return img_as_ubyte(np.concatenate((left, right), axis=1))
def do_the_learning(processed, model, preprocess):
    cropped = processed[processed.shape[0]//2 - 200:processed.shape[0]//2 + 200,processed.shape[1]//2 - 200:processed.shape[1]//2 + 200].copy()
    cv2.rectangle(processed,(processed.shape[1]//2 - 200,processed.shape[0]//2 - 200), (processed.shape[1]//2 + 200,processed.shape[0]//2 + 200),(0,0,255) )
    cropped = cv2.resize(cropped,(224,224))
    cropped = np.expand_dims(cropped, axis=0)
    cropped = preprocess(cropped)
    preds = model.predict(cropped)
    P = imagenet_utils.decode_predictions(preds)
    (imagenetID, label, prob) = P[0][0]
    cv2.putText(processed, "Label: {}, {:.2f}%".format(label, prob * 100),
	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    return processed