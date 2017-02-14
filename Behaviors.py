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

        # Resize
        small = cv2.resize(rThresh,    (9, 12), interpolation=cv2.INTER_AREA)

        # Debug
        big   = cv2.resize(  small, (640, 480), interpolation=cv2.INTER_AREA)  #Delete- for debug only
        cv2.imshow('frame', big)
        cv2.waitKey(5000)



    def __findLines(self):
        img   = self.rover.camera.read()
        print('doing')
        rImg  = VisionUtils.isolateColor(img,   [150, 75, 75],  [30, 255, 255])
        rGray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)
        ret, rThresh = cv2.threshold(rGray, 50, 255, cv2.THRESH_BINARY)

        # Test
        # small = cv2.resize(rThresh, (9, 12), interpolation=cv2.INTER_AREA)
        # big = cv2.resize(small, (640, 480), interpolation=cv2.INTER_AREA)  # Delete- for debug only
        # ret, big = cv2.threshold(big, 10, 255, cv2.THRESH_BINARY)

        # edges = cv2.Canny(big, 20, 40)


        cv2.imshow('Thresh', rThresh)


        # lines = cv2.HoughLinesP(edges, 1, np.pi, threshold=25, minLineLength=50, maxLineGap=10)
        lines = cv2.HoughLinesP(rThresh, 1, np.pi/50, threshold=100, minLineLength=200, maxLineGap=100)
        lines = [line[0] for line in lines]
        if lines is not None:
            print("Length:", len(lines))
            for x1, y1, x2, y2 in lines:

                # x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow('final', img)
            cv2.waitKey(5000)
        cv2.waitKey(1000)
        return lines

