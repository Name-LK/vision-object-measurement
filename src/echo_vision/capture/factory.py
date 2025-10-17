# Contains 'SensorFactory' Class
from echo_vision.interfaces.capturer_interface import Capturer
from echo_vision.drivers.kinectV1_driver import KinectV1Capturer
#from hololens_2 import HololensV2Capturer

class SensorFactory:
    """Factory that creates the correct capturer object"""
    @staticmethod
    def create_capturer(sensor_type: str, config: dict) -> Capturer:
        if sensor_type == "kinect_v1":
            return KinectV1Capturer(config)
        #elif sensor_type == "hololens_v2":
         #   return HololensV2Capturer()
        else:
            raise ValueError(f"Sensor type not found: {sensor_type}")