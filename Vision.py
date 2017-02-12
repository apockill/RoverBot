import time
import cv2
from picamera.array import PiRGBArray
from picamera       import PiCamera
from threading      import Thread, RLock



class Vision:
    def __init__(self):
        # Initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        # Threading
        self.stopThread = False
        self.mainThread = Thread(target=self.mainThread)
        self.mainThread.start()

    def mainThread(self):
        # Allow the camera to warmup
        time.sleep(0.1)

        # Capture Frames from the Camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # Grab the raw NumPy array representing the image
            image = frame.array

            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(5000) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break







