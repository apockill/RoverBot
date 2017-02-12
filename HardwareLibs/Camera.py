from HardwareLibs.RoboHat import startServos, stopServos, setServo
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2


class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

        # Initialize the frame and the variable used to indicate if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # Start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()


        # Wait until there is  frame loaded
        from time import sleep
        while self.frame is None: sleep(0.01)

        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # Grab the frame from the stream and clear the stream in preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # If the thread indicator variable is set, stop the thread and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # Return the frame most recently read
        return self.frame

    def close(self):
        # Indicate that the thread should be stopped
        print("PiVideoStream| Closing Video Thread")
        self.stopped = True


class PanTiltPiCamera(PiVideoStream):
    def __init__(self, panPin, tiltPin):
        super().__init__()
        super().start()

        self.panPin  = panPin
        self.tltPin = tiltPin

        startServos()

        # Set servos to the initial position
        self.panRot = -1
        self.tltRot = -1
        self.setPose(pan = 0, tilt = 0)

    def setPose(self, pan=None, tilt=None):
        if pan is not None and pan != self.panRot:
            setServo(self.panPin, pan)
            self.panRot = pan

        if tilt is not None and tilt != self.tltRot:
            setServo(self.tltPin, tilt)
            self.tltRot = tilt




    def close(self):
        super().close()
        print("PanTiltPiCamera| Stopping Servos")
        stopServos()
