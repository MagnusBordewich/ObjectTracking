import numpy as np
import cv2
import time

w=640
h=480

# This identifies the device and sets up the camera
my_camera = cv2.VideoCapture(0)
# The next two lines set the dimensions of the image to w*h pixels
my_camera.set(3,w)
my_camera.set(4,h)
# A short pause to allow the camera to warm up
time.sleep(2)

# A 'read' from the camera returns two things, a success indicator and the image
success, image = my_camera.read()
# Display the image on screen
cv2.imshow('View.png',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Is the image the right way up? If not, flip it. Try changing the -1 to 0 or 1.
image = cv2.flip(image,-1)
# We could apply a blur to remove noise
image = cv2.GaussianBlur(image,(55,55),0)
# Display the image on screen
cv2.imshow('View.png',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

my_camera.release()




