from echo_vision.utils.config_loader import load_config
from echo_vision.capture.factory import SensorFactory
from echo_vision.views.plotter import display_live_results
from echo_vision.utils.config_loader import load_config
from echo_vision.processing.segmentation import isolate_object
from echo_vision.processing.measurement import calculate_measurements
from echo_vision.views.plotter import display_results, display_live_results

def run_live_capture_pipeline():
    print("Startint Echo Vision (Live Mode)...")

    try:
        config = load_config('config.yaml')
        sensor_type = config.get('sensor', {}).get('type', 'kinect_v1')
        print(f"Using sensor: {sensor_type}")

        capturer = SensorFactory.create_capturer(sensor_type, config)

        display_live_results(capturer)
        
    except (ValueError, RuntimeError, FileNotFoundError) as e:
         print(f"Critical Error: {e}")

def run_measurement_pipeline():
    """Orchestrates the main flow of the measurement application."""
    print("Starting measurement application...")
    
    # 1. Load configurations
    config = load_config('config.yaml')

    try:
        # 2. Capture Layer
        print(f"Using sensor: {config['sensor']['type']}")
        capturer = SensorFactory.create_capturer(sensor_type=config['sensor']['type'], config=config)
        original_pcd = capturer.get_point_cloud()

        # 3. Processing Layer
        plane_cloud, object_cloud, roi_bbox = isolate_object(original_pcd, config)
        if object_cloud is None:
            print("Could not isolate an object. Exiting.")
            return
            
        measurements = calculate_measurements(object_cloud)
        if measurements is None:
            print("Could not calculate measurements. Exiting.")
            return

        # 4. Output/Visualization Layer
        print("Displaying results...")
        display_results(
            plane_cloud=plane_cloud,
            object_cloud=object_cloud,
            measurements=measurements,
            roi_bbox=roi_bbox
        )

    except (ValueError, RuntimeError, NotImplementedError) as e:
        print(f"A critical error occurred: {e}")