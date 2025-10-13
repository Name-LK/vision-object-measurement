# Defines abstract interface 'Capturer'
from abc import ABC, abstractmethod
import open3d as o3d

class Capturer(ABC):
    """Defines general interface for all capturer devices"""
    @abstractmethod
    def get_point_cloud(self) -> o3d.geometry.PointCloud:
        """Capture frames and returns a point cloud in open3D format"""
        pass