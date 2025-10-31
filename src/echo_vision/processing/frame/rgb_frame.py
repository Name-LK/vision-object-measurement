import cv2
import numpy as np

def get_frame(capturer):
    """Returns a RGB frame
    """
    try:
        rgb_frame = capturer.get_rgb_video()
        return rgb_frame
    except TypeError:
        print("\n[ERROR] Can't get a kinect RGB frame")
        exit()
    

    