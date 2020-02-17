import numpy as np
import cv2
import time
import os


# This system command loads the right drivers for the Raspberry Pi camera
os.system('sudo modprobe bcm2835-v4l2')

w=240
h=180

my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)

while (True):
    success, image = my_camera.read()
    image = cv2.flip(image,-1)
    image = cv2.GaussianBlur(image,(5,5),0)

    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_pink = np.array([166,50,50])
    upper_pink = np.array([174,255,255])
    mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
    mask = cv2.GaussianBlur(mask,(5,5),0)

    # findContours returns a list of the outlines of the white shapes in the mask (and a hierarchy that we shall ignore)
    # API differences:
    #   OpenCV 2.x: findContours -> contours, hierarchy
    #   OpenCV 3.x: findContours -> image, contours, hierarchy
    #   OpenCV 4.x: findContours -> contours, hierarchy
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # contours is a list, and each element is a set of coordinates for points on the boundary of an object 'join the dots' style.
    # we can draw the contours with the following command
    cv2.drawContours(image,contours,-1,(255,0,0),3)
    cv2.imshow('View',image)
    # Esc key to stop, otherwise repeat 
    key_pressed = cv2.waitKey(1)
    if key_pressed == 27:    
        break
    
cv2.destroyAllWindows()
my_camera.release()
# due to a bug in openCV you need to call wantKey three times to get the
# window to dissappear properly. Each wait only last 10 milliseconds
cv2.waitKey(10)
time.sleep(0.1)
cv2.waitKey(10)
cv2.waitKey(10)
