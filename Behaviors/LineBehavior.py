import cv2
import numpy as np
import VisionUtils
from Utils import lineAngle, clamp
from collections import namedtuple
from time import time, sleep


class Line:
    def __init__(self, p1, p2):
        # Point: [x, y] or (x, y)
        self.p1 = tuple(p1)
        self.p2 = tuple(p2)


        # Angle is 130 if the line points approximately from the bottom right to top left
        # Angle is 60 if the line points approximately from the bottom left to the top right
        self.angle = 180 - lineAngle(self.p1, self.p2)

    def __str__(self):
        return "Angle: " + str(self.angle) + "  P1: " + str(self.p1) + "  P2: " + str(self.p2)

    def __iter__(self):
        for point in [self.p1, self.p2]:
            yield point


class Mapper:
    """
    This class keeps track of new lines and identifies if the newly recognized line is consistent with the last
    few frames or if it's a mistake from bad line.

    It also performs the important task of keeping track of the map, where junctions are, and attempting to localize
    the robot within what it knows of the lines so far.
    """

    def __init__(self):
        self.history = []  # A list of line lists [[L1, L2], [L1, L2, L3] from previous frames
        self.currentLine = None

    def addLineFrame(self, lines):
        """
        :param lines: A list of [Line, Line] that the camera thinks it has found
        :return:
        """

        if len(lines) == 0:
            self.currentLine = None
            return


        self.history.append(lines)

        # Find the highest 'y' of any line
        highestY = (0, 0)  # [0] is the line index, [1] is the highest y value
        for index, line in enumerate(self.history[-1]):
            if line.p1[1] > highestY[1]:
                highestY = (index, line.p1[1])
            elif line.p2[1] > highestY[1]:
                highestY = (index, line.p2[1])
        self.currentLine = self.history[-1][highestY[0]]

    def getCurrentLine(self):
        return self.currentLine


class FollowLine:

    def __init__(self, parent):
        self.rover = parent
        self.map   = Mapper()
        self.targetSpeed = 300

        self.framesSinceLine = 0  # How many frames since the line was seen


    def update(self):
        lowRed  = [150, 75, 75]
        highRed = [30, 255, 255]

        lines = self.__findLines(lowRed, highRed)
        self.map.addLineFrame(lines)

        line = self.map.getCurrentLine()  # Gets direction of the currently followed line

        if line is None:
            self.framesSinceLine += 1
            if self.framesSinceLine > 50:
                self.rover.LWheel.setSpeed(0)
                self.rover.RWheel.setSpeed(0)
            return

        self.framesSinceLine = 0

        # Pick the point to move towards
        highestPoint = sorted(line, key=lambda l: l[1])[0]
        print(line, highestPoint)
        self.moveTowards(highestPoint)


    # Robot Control Functions
    def moveTowards(self, point):
        """
        Move towards a Line
        :param point: [x, y]
        :return:
        """

        lWheel = self.rover.LWheel
        rWheel = self.rover.RWheel

        # Get the highest point of the line
        horzMiddle = self.rover.camera.resolution[0] / 2
        vertMax = self.rover.camera.resolution[1]
        xMag   = (point[0] - horzMiddle) / horzMiddle     # -1 to 1, where -1 is left and 1 is right
        yMag   = (vertMax - point[1]) / vertMax           # 0 to 1, where 1 is toop and 0 is bottom


        turnSpeed  = (self.targetSpeed * .4) * xMag # * yMag # clamp(self.targetSpeed * yMag, self.targetSpeed*.5, self.targetSpeed)
        lSpeed = self.targetSpeed*.6 + turnSpeed  # Where -1 xmag will lower left turning speed
        rSpeed = self.targetSpeed*.6 - turnSpeed  # Where -1 xmag will raise the right turning speed
        lSpeed = clamp(int(lSpeed), -self.targetSpeed * .1, self.targetSpeed)
        rSpeed = clamp(int(rSpeed), -self.targetSpeed * .1, self.targetSpeed)

        # Make sure stuff doesn't get too fast!
        if lSpeed + rSpeed >= self.targetSpeed * 2:
            amountOver = lSpeed + rSpeed - self.targetSpeed * 2
            lSpeed -= amountOver / 2
            rSpeed -= amountOver / 2

        lWheel.setSpeed(lSpeed)
        rWheel.setSpeed(rSpeed)

        print("Left: ", lSpeed, "\tRight: ", rSpeed, "\txMag", xMag, "\tyMag", yMag)

        # if point[0] < horzMiddle:
        #     print("Left")
        #     lWheel.setSpeed(0)
        #     rWheel.setSpeed(self.targetSpeed)
        #     return
        #
        # if point[0] > horzMiddle:
        #     print("Right")
        #     lWheel.setSpeed(self.targetSpeed)
        #     rWheel.setSpeed(0)
        #     return

        """
        lowerThresh = 89
        upperThresh = 91
        # Straight
        if lowerThresh <= line.angle <= upperThresh:
            print("Straight")
            lWheel.setSpeed(self.targetSpeed)
            rWheel.setSpeed(self.targetSpeed)
            return

        # Left
        if line.angle < lowerThresh:
            print("Left")
            lWheel.setSpeed(self.targetSpeed*.5)
            rWheel.setSpeed(self.targetSpeed)
            return

        # Right
        if line.angle > upperThresh:
            print("Right")
            lWheel.setSpeed(self.targetSpeed)
            rWheel.setSpeed(self.targetSpeed*.5)
            return
        """

    # Line Identification Functions
    def __findLines(self, hueLow, hueHigh):
        img   = self.rover.camera.read()

        rImg  = VisionUtils.isolateColor(img,   hueLow,  hueHigh)
        rGray = cv2.cvtColor(rImg, cv2.COLOR_BGR2GRAY)
        ret, rThresh = cv2.threshold(rGray, 50, 255, cv2.THRESH_BINARY)

        # Make the image small to reduce line-finding processing times
        small = cv2.resize(rThresh, (64, 48), interpolation=cv2.INTER_AREA)




        # lines = cv2.HoughLinesP(edges, 1, np.pi, threshold=25, minLineLength=50, maxLineGap=10)
        lines = cv2.HoughLinesP(small, 1, np.pi/200, threshold=25, minLineLength=20, maxLineGap=10)


        if lines is None: return []

        # If lines were found, combine them until you have 1 average for each 'direction' of tape in the photo
        lines = [line[0] for line in lines]
        combinedLines = self.__combineLines(lines)


        return combinedLines

    def __combineLines(self, unsortedLines):
        """ Combines similar lines into one large 'average' line """

        maxAngle = 45
        minLinesForCombo = 5

        def getAngle(line):
            # Turn angle from -180:180 to just 0:180
            angle = lineAngle(line[:2], line[2:])
            if angle < 0: angle += 180
            return angle

        def lineFits(checkLine, combo):
            """ Check if the line fits within this group of combos by checking it's angle """
            checkAngle = getAngle(checkLine)
            for line in combo:
                angle = lineAngle(line[:2], line[2:])
                difference = abs(checkAngle - angle)

                if difference < maxAngle or 180 - difference < maxAngle:
                    return True
                # if difference > maxAngle * 2 or 180 - difference > maxAngle * 2:
                #     return False
            return False

        # Pre-process lines so that lines always point from 0 degrees to 180, and not over
        for i, line in enumerate(unsortedLines):
            angle = lineAngle(line[:2], line[2:])
            if angle < 0:
                line = np.concatenate((line[2:], line[:2]))
                unsortedLines[i] = line


        # Get Line Combos
        lineCombos = []  # Format: [[[l1, l2, l3], [l4, l5, l6]], [[line 1...], [line 2...]]]

        while len(unsortedLines) > 0:
            checkLine = unsortedLines.pop(0)

            isSorted = False
            for i, combo in enumerate(lineCombos):
                if lineFits(checkLine, combo):
                    # Process the line so that the [x1, y1, and x2, y2] are in the same positions as other combos
                    lineCombos[i].append(checkLine.tolist())
                    isSorted = True
                    break

            if not isSorted:
                lineCombos.append([checkLine.tolist()])


        # # Limit each combo to minSamples, keeping only the longest lines
        # lineCombos = [sorted(combo, key= lambda c: (c[0] - c[2]) ** 2 + (c[1] - c[3]) ** 2, reverse=True)
        #               for combo in lineCombos]
        # lineCombos = [combo[:minLinesForCombo] for combo in lineCombos]


        # Filter and Average Combo Groups Format: [[L1], [L2], [L3]]
        averagedCombos = []
        for combo in lineCombos:
            if len(combo) < minLinesForCombo: continue

            avgLine = (np.sum(combo, axis=0) / len(combo)).astype(int)
            avgLine *= 10  # Rescale to screen size
            averagedCombos.append(Line(avgLine[:2], avgLine[2:]))


        # # Draw Line Combos and Final Lines
        # img = self.rover.camera.read()
        # for i, combo in enumerate(lineCombos):
        #     for x1, y1, x2, y2 in combo:
        #         x1 *= 10
        #         y1 *= 10
        #         x2 *= 10
        #         y2 *= 10
        #
        #         cv2.line(img, (x1, y1), (x2, y2), (80*i, 80*i, 80*i), 2)
        #
        # if len(averagedCombos):
        #     for p1, p2 in averagedCombos:
        #         x1 = p1[0]
        #         y1 = p1[1]
        #         x2 = p2[0]
        #         y2 = p2[1]
        #
        #         cv2.line(img, (x1, y1), (x2, y2), (80, 80, 80), 8)
        #
        # cv2.imshow('final', img)
        # cv2.waitKey(2500)

        return averagedCombos





