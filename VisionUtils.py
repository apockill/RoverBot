import numpy as np
import cv2


def autoCanny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def isolateColor(img, lower, upper):
    """

    :param img: Image to isolate teh color of
    :param lower: [lowerHue, lowerSat, lowerVal]
    :param upper: [upperHue, upperSat, upperVal]
    :return: Isolated image
    """

    # Isolate the red
    hsv   = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask  = cv2.inRange(hsv, lower, upper)
    final = cv2.bitwise_and(img, img, mask=mask)

    return final