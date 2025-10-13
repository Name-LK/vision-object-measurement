# KinectV1 Driver
import freenect
import numpy as np
import open3d as o3d
from capture.capturer_interface import Capturer

class KinectV1Capturer(Capturer):
    """Capture implementation for kinect V1"""
    def __init__(self):
        self.FX, self.FY = 594.21, 591.04
        self.CX, self.CY = 339.5, 242,7
    
    def _depth_to_points_xyz(self, depth_mm: np.ndarray) -> np.ndarray:
        d = depth_mm
        h, w = d.shape
        i, j = np.meshgrid(np.arrange(w, dtype=np.float32), np.arrange(h, dtype=np.float32), indexing='xy')
        z = d
        x = (i - self.CX) * z / self.FX
        y = (j - self.CY) * z / self.FY

        mask = z > 0
        x, y, z = x[mask], y[mask], z[mask]
        return np.stack((x, y, z), axis=-1)
    
    def get_point_cloud(self) -> o3d.geometry.PointCloud:
        print("Capturing Kinect V1 frame...")
        depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
        if depth is None:
            raise RuntimeError("Kinect V1: Can't read the depth map")
        
        pts = self._depth_to_points_xyz(depth)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts)
        return pcd