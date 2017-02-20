import numpy as np
import cv2
import time

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

    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    colour = str(image_HSV[h//2][w//2])
    cv2.line(image,(0,h//2),(w-1,h//2),[255,255,255])        
    cv2.line(image,(w//2,0),(w//2,h-1),[255,255,255])
    cv2.putText(image,colour,(10,30),cv2.FONT_HERSHEY_PLAIN,1,[255,255,255])
    cv2.imshow('View',image)
    # Esc key to stop, otherwise repeat after 1 milliseconds
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
