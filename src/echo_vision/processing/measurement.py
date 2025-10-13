# Functions to calculate OBB, area, volume, etc...
import numpy as np
from scipy.spatial import ConvexHull

def calculate_measurements(object_cloud):
    """Calc 2D dimensions from a object points cloud"""

    if len(object_cloud.points) < 10:
        print("Warning: A few points on the object to calculate")
        return None
    
    # Removes "Noise"
    cloud_cleaned = object_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)[0]
    print(f"Isolated object points: {len(cloud_cleaned.points)}.")

    if len(cloud_cleaned.points) < 10:
        return None
    
    # Calcs oriented bounding box (OBB)
    obb = cloud_cleaned.get_oriented_bounding_box()
    dims = obb.extent
    length = max(dims)
    width = sorted(dims)[1]

    # Calcs base area
    object_points_2d = np.asarray(cloud_cleaned.points)[:, :2]
    area = 0
    if len(object_points_2d) >= 4:
        hull_2d = ConvexHull(object_points_2d, qhull_options='QJ')
        area = hull_2d.volume
    
    measurements = {
        "length": length,
        "width": width,
        "area": area,
        "obb": obb, # Passes the OBB object to the view layer
        "clean_cloud": cloud_cleaned # Passes the cleaned point cloud
    }
    
    print("\n--- 2D Measurements ---")
    print(f"Length: {length:.1f} mm")
    print(f"Width:     {width:.1f} mm")
    print(f"Base area (estimate): {area / 100:.1f} cm²\n")
    
    return measurements