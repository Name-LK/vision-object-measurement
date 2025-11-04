# KinectV1 Driver
import freenect
import numpy as np
import open3d as o3d
from echo_vision.interfaces.capturer_interface import Capturer

class KinectV1Capturer(Capturer):
    """Capture implementation for kinect V1"""
    def __init__(self, config: dict):
        self.FX, self.FY = 594.21, 591.04
        self.CX, self.CY = 339.5, 242.7

        sensor_config = config.get('sensor', {})
        self.step = sensor_config.get('step_downsample', 4)
        self.z_min = sensor_config.get('z_min_cutoff', 500.0)
        self.z_max = sensor_config.get('z_max_cutoff', 4000.0)
    
    def _depth_to_points_xyz(self, depth_mm: np.ndarray) -> np.ndarray:
        d = depth_mm[::self.step, ::self.step]
        h, w = d.shape
        i, j = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32), indexing='xy')
        z = d
        '''x = (i - self.CX) * z / self.FX
        y = (j - self.CY) * z / self.FY'''

        x = (i * self.step - self.CX) * z / self.FX
        y = (j * self.step - self.CY) * z / self.FY

        #mask = z > 0
        mask = (z > 0) & np.isfinite(z) & (z >= self.z_min) & (z <= self.z_max)
        x, y, z = x[mask], y[mask], z[mask]
        return np.stack((x, y, z), axis=-1)
    
    def get_point_cloud(self) -> o3d.geometry.PointCloud:
        print("Capturing Kinect V1 frame...")
        depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
        if depth is None:
            raise RuntimeError("Kinect V1: Can't read the depth map")
        
        pts = self._depth_to_points_xyz(depth.astype(np.float32))

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts)
        return pcd
    
    def get_rgb_frame(self):
        """Returns the RGB video frame"""
        array, _ = freenect.sync_get_video()
        return array