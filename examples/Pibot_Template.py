from BrickPi import *
import threading
import numpy as np
import cv2
import time
import os

# Set up the BrickPi
BrickPiSetup()  
BrickPi.MotorEnable[PORT_A] = 1 
BrickPi.MotorEnable[PORT_B] = 1 
BrickPiSetupSensors()
#This thread is used for keeping the motors running
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while True:
            BrickPiUpdateValues()       
            time.sleep(.1)              
thread1 = myThread(1, "Thread-1", 1)    
thread1.setDaemon(True)
thread1.start()


# Set up the camera
os.system('sudo modprobe bcm2835-v4l2')
w=240
h=160
lower_pink = np.array([166,50,50])
upper_pink = np.array([174,255,255])
my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)


# The main loop below analyses a frame of video and sets the motor speeds accordingly
while True:
    target_x=w/2
    success, image = my_camera.read()
    image = cv2.flip(image,-1)
    image = cv2.GaussianBlur(image,(5,5),0)
    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
    mask = cv2.GaussianBlur(mask,(5,5),0)
    # findContours returns a list of the outlines of the white shapes in the mask (and a heirarchy that we shall ignore)            
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # If we have at least one contour, look through each one and pick the biggest
    if len(contours)>0:
        largest = 0
        area = 0
        for i in range(len(contours)):
            # get the area of the ith contour
            temp_area = cv2.contourArea(contours[i])
            # if it is the biggest we have seen, keep it
            if temp_area>area:
                area=temp_area
                largest = i
        # Compute the x coordinate of the center of the largest contour
        coordinates = cv2.moments(contours[largest])
        target_x = int(coordinates['m10']/coordinates['m00'])
    if target_x < w/2: # target is to the left of centre
        BrickPi.MotorSpeed[PORT_A] = -200  # Set motors to turn left
        BrickPi.MotorSpeed[PORT_B] = 200   
    elif target_x > w/2: # target is to the right of centre
        BrickPi.MotorSpeed[PORT_A] = 200  # Set motors to turn right
        BrickPi.MotorSpeed[PORT_B] = -200       
    else:
        BrickPi.MotorSpeed[PORT_A] = 0  # Set motors to stop
        BrickPi.MotorSpeed[PORT_B] = 0       
    # Esc key to stop, otherwise repeat loop after 1 milliseconds
    key_pressed = cv2.waitKey(1)
    if key_pressed == 27:    
        break