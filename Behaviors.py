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

        edges = cv2.Canny(gray, 15, 35)





        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        if lines is None:
            cv2.imshow('Edge', edges)
            # cv2.imshow('Frame', gray)
            cv2.waitKey(500)
            return

        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        print("Found lines: ", len(lines))

        cv2.imshow('Edge', img)
        cv2.waitKey(1500)