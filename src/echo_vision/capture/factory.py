# Contains 'SensorFactory' Class
from capturer_interface import Capturer
from drivers.kinectV1_driver import KinectV1Capturer
#from hololens_2 import HololensV2Capturer

class SensorFactory:
    """Factory that creates the correct capturer object"""
    @staticmethod
    def create_capturer(sensor_type: str) -> Capturer:
        if sensor_type == "kinect_v1":
            return KinectV1Capturer()
        #elif sensor_type == "hololens_v2":
         #   return HololensV2Capturer()
        else:
            raise ValueError(f"Sensor type not found: {sensor_type}")