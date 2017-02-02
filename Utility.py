

def clamp(val, low, max):
    # Clamp a value between a min and max

    if val < low:
        return low

    elif val > max:
        return max

    return val


def sign(val):
    # Return the sign of a value. 0 is positive
    if val < 0:
        return -1
    return 1