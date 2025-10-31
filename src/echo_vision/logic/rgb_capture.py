from echo_vision.utils.config_loader import load_config
from echo_vision.capture.factory import SensorFactory
from echo_vision.views.plotter import display_live_rgb_capture

#Needed steps -> load_config - get sensor type of the loaded config - create the Capturer - pass the capturer to the rgb plotter method
def rgb_live_pipeline():
    try:
        config = load_config('config.yaml')
        sensor_type = config.get("sensor", {}).get("type", "kinect_v1")
        capturer = SensorFactory.create_capturer(sensor_type, config)
        display_live_rgb_capture(capturer=capturer)
        
    except (ValueError, RuntimeError, FileNotFoundError) as e:
         print(f"Critical Error: {e}")