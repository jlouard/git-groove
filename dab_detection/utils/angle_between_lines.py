import math

def angle_between_lines(x1, y1, x2, y2, x3, y3):
    # Calculate the slopes of the two lines
    slope1 = (y2 - y1) / (x2 - x1)
    slope2 = (y3 - y2) / (x3 - x2)
    
    # Calculate the angle between the two lines
    angle = math.atan2(slope2 - slope1, 1 + slope1 * slope2)
    
    # Convert the angle to degrees and return it
    return math.degrees(angle) 