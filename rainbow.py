from piwars_bot import Robot
from piwars_bot_controller import PiWarsController
from piwars_bot_display import RobotDisplay
import cv2
import numpy as np

def npcol(r, g, b):
    return np.array([r,g,b], np.uint8)

def get_red_filter(hsv_image):
    mask1 = cv2.inRange(hsv_image, (165, 30, 80), (180, 230, 255))
    mask2 = cv2.inRange(hsv_image, 0, 15)
    return cv2.bitwise_or(mask1, mask2)

def get_green_filter(hsv_image):
    pass

def get_blue_filter(hsv_image):
    pass

def get_yellow_filter(hsv_image):
    pass

def main():
    # setup the robot
    hue_ranges = [ # Each is a list of lists - only really needed for 
        # red
        # blue
        # yellow
        # green
    ]
    # while we can run
        # 

if __name__ == "__main__":
    main()