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

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if lower[0] > upper[0]:
        # If the HSV values wrap around, then intelligently mask it

        upper1 = [180, upper[1], upper[2]]
        mask1  = cv2.inRange(hsv, np.array(lower), np.array(upper1))

        lower2 = [0, lower[1], lower[2]]
        mask2  = cv2.inRange(hsv, np.array(lower2), np.array(upper))

        mask = mask1 + mask2

    else:
        mask  = cv2.inRange(hsv, np.array(lower), np.array(upper))


    final = cv2.bitwise_and(img, img, mask=mask)
    return final