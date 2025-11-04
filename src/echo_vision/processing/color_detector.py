import cv2
import numpy as np

def detect_objects_by_color(frame: np.ndarray, config: dict):
    """_summary_

    Args:
        frame (np.ndarray): _description_
        config (dict): _description_

    Returns:
        frame: _description_
        
    """
    config = config.get('color_detection', {})
    lower_hsv = np.array(config.get('lower_hsv', [0, 0, 0]))
    upper_hsv = np.array(config.get('upper_hsv', [179, 255, 255]))
    min_area = config.get('min_area', 500)

    # Convert BRG frame color to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create the color mask
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Find mask contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Proccess the biggest detected contour
    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > min_area:
            (x, y, w, h) = cv2.boundingRect(c)
            
            # Draw the rectangle around the detected object in original frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Object Detected", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return frame, mask