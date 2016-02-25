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
        # Compute the coordinates of the center of the largest contour
        coordinates = cv2.moments(contours[largest])
        target_x = int(coords['m10']/coords['m00'])
        target_y = int(coords['m01']/coords['m00'])
        # Pick a suitable diameter for our target (grows with the contour)
        diam = int(np.sqrt(area)/4)
        # draw on a target
        cv2.circle(image,(target_x,target_y),diam,(0,255,0),1)
        cv2.line(image,(target_x-2*diam,target_y),(target_x+2*diam,target_y),(0,255,0),1)
        cv2.line(image,(target_x,target_y-2*diam),(target_x,target_y+2*diam),(0,255,0),1)

 # Esc key to stop, otherwise repeat after 33 milliseconds
    key_pressed = cv2.waitKey(33)
    if key_pressed == 27:    
        break
    
cv2.destroyAllWindows()
