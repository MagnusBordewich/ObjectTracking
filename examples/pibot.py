import numpy as np
import copy
import cv
import cv2
import time
import os
import StringIO
from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import threading
os.system('sudo modprobe bcm2835-v4l2')
side = 0
w=80
h=60
turning_rate = 60
running = False

BrickPiSetup()  # setup the serial port for communication
BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D
#This thread is used for keeping the motors running
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while running:
            BrickPiUpdateValues()       # Ask BrickPi to update values for senso
            #time.sleep(.1)              # sleep for 200 ms

thread1 = myThread(1, "Thread-1", 1)            #Setup and start the thread
thread1.setDaemon(True)
thread1.start()

# This sets up the video capture
cap = cv2.VideoCapture(0)
cap.set(3,w)
cap.set(4,h)
time.sleep(2)
#cap.set(15,-80.0)

# Main loop
while True:
    try:
        found = False
        ret, image = cap.read()
        image = cv2.flip(image,-1)
        #image2 = copy.deepcopy(image) 
        #image2 = cv2.cvtColor(image2,cv2.COLOR_RGB2BGR)
        binary = cv2.GaussianBlur(image,(5,5),0)
        binary = cv2.cvtColor(binary,cv2.COLOR_BGR2HSV)
        lower_pink = np.array([164,50,50])
        upper_pink = np.array([176,255,255])
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.inRange(binary,lower_pink,upper_pink)
        mask = cv2.erode(mask,kernel,iterations=1)
        mask = cv2.dilate(mask,kernel,iterations=1)
        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        blob_x = w/2
        area = 0
        if len(contours)>0:
            largest = 0
            area = cv2.contourArea(contours[0])
            if len(contours)>1:
                for i in range(1,len(contours)):
                    temp_area = cv2.contourArea(contours[i])
                    if temp_area>area:
                        area=temp_area
                        largest = i
            if area > 100:
                found=True
                coords = cv2.moments(contours[largest])
                blob_x = int(coords['m10']/coords['m00'])
                #blob_y = int(coords['m01']/coords['m00'])
                #diam = int(np.sqrt(area)/4)
                #cv2.circle(image,(blob_x,blob_y),diam,(0,255,0),1)
                #cv2.line(image,(blob_x-2*diam,blob_y),(blob_x+2*diam,blob_y),(0,255,0),1)
                #cv2.line(image,(blob_x,blob_y-2*diam),(blob_x,blob_y+2*diam),(0,255,0),1)
            #cv2.drawContours(image,contours,largest,(255,0,0),3)

        if not found:
            if side == 0:
                L_motor_speed=-70
                R_motor_speed=70
            else:
                L_motor_speed=70
                R_motor_speed=-70
        elif area > 2000:
            direction = blob_x -w/2
            if direction < -w/4:
                L_motor_speed=-80
                R_motor_speed=80
                pass
            elif direction > w/4:
                L_motor_speed=80
                R_motor_speed=-80
            else:
                L_motor_speed=0
                R_motor_speed=0
        else:
            direction = blob_x -w/2
            if direction <0:
                side = 0
            else:
                side = 1
            L_motor_speed=max(0,min(170+(direction*turning_rate/w),255))
            R_motor_speed=max(0,min(170-(direction*turning_rate/w),255))
        BrickPi.MotorSpeed[PORT_A] = L_motor_speed
        BrickPi.MotorSpeed[PORT_D] = R_motor_speed
        found = False
    except KeyboardInterrupt:
        break


