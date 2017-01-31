from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Let the camera warm up
time.sleep(0.1)

# Get image from camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# Display the image
cv2.imshow("Image", image)
cv2.waitKey(0)