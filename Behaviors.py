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


    def __findLineDirections(self):
        # Inputs

        # Possible Pairs (8,6) (9,12) (12,16)
        gridW = 9
        gridH = 12


        # Processing
        img = self.rover.camera.read()

        rImg = VisionUtils.isolateColor(img, [150, 75, 75], [30, 255, 255])
        rGray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)
        ret, rThresh = cv2.threshold(rGray, 50, 255, cv2.THRESH_BINARY)


        small = cv2.resize(rThresh,    (9, 12), interpolation=cv2.INTER_AREA)

        # Debug
        big   = cv2.resize(  small, (640, 480), interpolation=cv2.INTER_AREA)  #Delete- for debug only
        cv2.imshow('frame', big)
        cv2.waitKey(5000)



    def __findLines(self):
        img   = self.rover.camera.read()

        rImg  = VisionUtils.isolateColor(img,   [150, 75, 75],  [30, 255, 255])
        rGray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)
        ret, rThresh = cv2.threshold(rGray, 50, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(rThresh, 20, 40)

        cv2.imshow('Thresh', rThresh)


        # lines = cv2.HoughLinesP(edges, 1, np.pi, threshold=25, minLineLength=50, maxLineGap=10)
        lines = cv2.HoughLinesP(edges, 1, np.pi/1000, threshold=40, minLineLength=100, maxLineGap=100)

        if lines is not None:
            print("Length:", lines)
            for line in lines:
                print(line)
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow('final', img)
            cv2.waitKey(5000)
        return lines

