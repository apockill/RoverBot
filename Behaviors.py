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

        rImg  = VisionUtils.isolateColor(img,   [150, 50, 50],  [30, 255, 255])


        # ret, rThresh = cv2.threshold(rImg, 90, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(rImg, 20, 40)

        # cv2.imshow('t', rThresh)
        cv2.imshow('r', rImg)
        cv2.imshow('e', edges)
        lines = cv2.HoughLines(image=edges, rho=1, theta=np.pi/180, threshold=100) # 1, np.pi / 180, 200)
        if lines is None:
            # cv2.imshow('Frame', gray)
            cv2.waitKey(3000)
            return




        for line in lines[:10]:
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
        cv2.waitKey(4500)

