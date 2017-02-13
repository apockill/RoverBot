import cv2
import numpy as np
import VisionUtils


class FollowLine:
    def __init__(self, parent):
        self.rover = parent


    def isUpdate(self):
        pass

    def update(self):
        self.__findLines()

    def __findLines(self):
        print("Doing thing!")

        img   = self.rover.camera.read()
        gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 50, 240)

        cv2.imshow('LinedImage', edges)
        cv2.imshow('Frame', gray)
        cv2.waitKey(500)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        if lines is None: return None

        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        print("Found: ", lines)

        cv2.imshow('LinedImage', img)
        cv2.waitKey(5000)