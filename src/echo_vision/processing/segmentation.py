# Functions to segmentate the plan and isolate the object
import numpy as np
import open3d as o3d

def isolate_object(pcd: o3d.geometry.PointCloud, config: dict):
    """Aply ROI, segment the plan and isolate the main object

    Args:
        pcd (o3d.geometry.PointCloud): _description_
        config (dict): _description_
    """

    # Aply FOV filter (ROI)
    roi_cfg = config['roi_bounds']
    bbox = o3d.geometry.AxisAlignedBoundingBox(
        min_bound=(roi_cfg["min_x"], roi_cfg["min_y"], roi_cfg["min_z"]),
        max_bound=(roi_cfg["max_x"], roi_cfg["max_y"], roi_cfg["max_z"])
    )

    pcd_cropped = pcd.crop(bbox)
    print(f"Points after cutting (ROI): {len(pcd_cropped.points)}.")

    if len(pcd_cropped.points) < 100:
        print("ERROR: A few points detected in the region of interest")
        return None, None, bbox
    
    # Segment the plan

    proc_cfg = config['processing']
    plane_model, inliers = pcd_cropped.segment_plane(
        distance_threshold=proc_cfg['plane_distance_threshold'],
        ransac_n=3,
        num_iterations=1000
    )

    plane_cloud = pcd_cropped.select_by_index(inliers)
    object_cloud = pcd_cropped.select_by_index(inliers, invert=True)

    return plane_cloud, object_cloud, bbox