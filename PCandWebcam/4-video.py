import numpy as np
import cv2
import time
import Image

w=640
h=480

my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)

while (True):
    success, image = my_camera.read()
    image = cv2.flip(image,-1)
    image = cv2.GaussianBlur(image,(5,5),0)

    image_HSV = cv2.cvtColor(binary,cv2.COLOR_BGR2HSV)
    lower_pink = np.array([166,50,50])
    upper_pink = np.array([174,255,255])
    mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
    mask = cv2.GaussianBlur(mask,(5,5),0)
            
    LRarray = np.sum(mask,axis=0)/255
    max_x_intensity = 0
    max_x_coordinate = 0
    for i in range(w):
        if LRarray[i]>max_x_intensity:
            max_x_coordinate=i
            max_x_intensity=LRarray[i]
            
    cv2.line(image,(max_x_coordinate,0),(max_x_coordinate,h-1),[255,255,255])
    cv2.imshow('View.png',image)
    # Esc key to stop, otherwise repeat after 33 milliseconds
    key_pressed = cv2.waitKey(33)
    if key_pressed == 27:    
        break
    
cv2.destroyAllWindows()
