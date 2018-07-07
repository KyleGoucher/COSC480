import vrep
import cv2
import sys
import numpy as np
import time
import random
import math


vrep.simxFinish(-1)
# connects to vrep
clientID = vrep.simxStart('127.0.0.1',19997,True, True,5000,5)

if clientID != -1:
    print("Connection Established!")

else:
    sys.exit("Error: No connection could be established")
# gathers object handles
_, J1_handle = vrep.simxGetObjectHandle(clientID, 'J1', vrep.simx_opmode_oneshot_wait)
_, J2_handle = vrep.simxGetObjectHandle(clientID, 'J2', vrep.simx_opmode_oneshot_wait)
_, J3_handle = vrep.simxGetObjectHandle(clientID, 'J3', vrep.simx_opmode_oneshot_wait)
_, J4_handle = vrep.simxGetObjectHandle(clientID, 'J4', vrep.simx_opmode_oneshot_wait)
_, cam_handle = vrep.simxGetObjectHandle(clientID, 'Vision1', vrep.simx_opmode_oneshot_wait)

while(1):
    vrep.simxSetJointPosition(clientID, J1_handle, math.radians(random.randint(0, 360)), vrep.simx_opmode_oneshot)
    vrep.simxSetJointPosition(clientID, J2_handle, math.radians(random.randint(-65, 65)), vrep.simx_opmode_oneshot)
    vrep.simxSetJointPosition(clientID, J3_handle, math.radians(random.randint(0, 360)), vrep.simx_opmode_oneshot)
    vrep.simxSetJointPosition(clientID, J4_handle, math.radians(random.randint(0, 360)), vrep.simx_opmode_oneshot)
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, cam_handle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    # saves camera frame, rotates image and converts to BGR
    _, resolution, image =vrep.simxGetVisionSensorImage(clientID,cam_handle,0, vrep.simx_opmode_buffer)
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # converts img to hsv and detect colors
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green_low = np.array([49, 50, 50], dtype=np.uint8)
    green_high = np.array([80, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, green_low, green_high)
    cv2.imshow('Image', img)
    cv2.imshow('Mask', mask)
    # runs until ESC key is pressed and sets robot back to start position
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        vrep.simxSetJointPosition(clientID, J1_handle, 0, vrep.simx_opmode_oneshot)
        vrep.simxSetJointPosition(clientID, J2_handle, 0, vrep.simx_opmode_oneshot)
        vrep.simxSetJointPosition(clientID, J3_handle, 0, vrep.simx_opmode_oneshot)
        vrep.simxSetJointPosition(clientID, J4_handle, 0, vrep.simx_opmode_oneshot)
        time.sleep(2)
        print("Process stopped by user")
        break











