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
# Is the image the right way up? If not, flip it. Try changing the -1 to 0 or 1.
image = cv2.flip(image,-1)
# Display the image on screen
cv2.imshow('View',image)
cv2.waitKey(0)

# We could apply a blur to remove noise
image = cv2.GaussianBlur(image,(5,5),0)

# change the colour space to HSV
image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
# print the HSV values of the middle pixel
print('Middle pixel HSV: ',image_HSV[h//2][w//2])
# define the range of hues to detect - adjust these to detect different colours
lower_pink = np.array([160,50,50])
upper_pink = np.array([175,255,255])
# create a mask that identifies the pixels in the range of hues
mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
mask_inverted=cv2.bitwise_not(mask)
# Create a grey image and black out the masked area
image_grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image_grey = cv2.bitwise_and(image_grey,image_grey,mask=mask_inverted)
# Black out unmasked area of original image
image_masked=cv2.bitwise_and(image,image,mask=mask)

# Combined the two images
image_grey = cv2.cvtColor(image_grey,cv2.COLOR_GRAY2BGR)
image_combined = cv2.add(image_grey,image_masked)

cv2.imshow('View',image_combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
my_camera.release()
# due to a bug in openCV you need to call wantKey three times to get the
# window to dissappear properly. Each wait only last 10 milliseconds
cv2.waitKey(10)
time.sleep(0.1)
cv2.waitKey(10)
cv2.waitKey(10)
