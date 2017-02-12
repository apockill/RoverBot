import cv2

class FollowLine:
    def __init__(self, rover):
        self.rover = rover


    def isUpdate(self):
        pass

    def update(self):
        frame = self.rover.camera.read()
        cv2.imshow('Main', frame)
        cv2.waitKey(3500)