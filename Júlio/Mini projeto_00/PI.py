import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I
import matplotlib.pyplot as plt # Matplotlib
import numpy as np # Numpy
from scipy import ndimage

print('program started')
captura = cv2.VideoCapture(0)

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
print ('Connected to remote API server')
r, colorCam = vrep.simxGetObjectHandle(clientID, "kinect_rgb", vrep.simx_opmode_oneshot_wait);
r, leftmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait);
r, rightmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait);

vrep.simxSetJointTargetVelocity(clientID, leftmotor, 0, vrep.simx_opmode_streaming);
vrep.simxSetJointTargetVelocity(clientID, rightmotor, 0, vrep.simx_opmode_streaming);

r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_streaming);
time.sleep(0.5)

while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)
	img_threshold = cv2.threshold(mat2,127,255,cv2.THRESH_BINARY)
	#print(mat2[0,1])
	#mat2[0,320] = 220
	##print(resolution[0]) #640
	#print(resolution[1]) #480 

    ret, frame = captura.read();
    cv2.imshow("Video", frame)
   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
 
captura.release()
cv2.destroyAllWindows()


	cv2.imshow('robot camera', cv2.flip( mat2, 0 ))	
	cv2.imshow('robot camera img_threshold', cv2.flip( img_threshold[1], 0 ))
	
	for u in range(640):
		if(img_threshold[1][0, u] == 0):
			porcL = u/640;
			porcR = 1-porcL;
			vrep.simxSetJointTargetVelocity(clientID, leftmotor, 6.7*porcL, vrep.simx_opmode_streaming);
			vrep.simxSetJointTargetVelocity(clientID, rightmotor, 6.7*porcR, vrep.simx_opmode_streaming);
			#print(porcL)
			#print(porcR)
			break

	cv2.waitKey(1)