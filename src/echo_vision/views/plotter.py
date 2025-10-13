# Rules to create and show the 3D scene
import numpy as np
import pyvista as pv

def display_results(plane_cloud, object_cloud, measurements, roi_bbox):
    """Create and display the 3D scene with the results using PyVista."""
    
    plotter = pv.Plotter(window_size=[1280, 720])
    plotter.set_background('black')

    # Convert point clouds to PyVista format
    pv_plane = pv.PolyData(np.asarray(plane_cloud.points))
    # Use the clean point cloud returned from the measurements
    pv_object = pv.PolyData(np.asarray(measurements['clean_cloud'].points))

    # Create the Oriented Bounding Box (OBB) mesh
    obb = measurements['obb']
    pv_obb = pv.Box(bounds=(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5))
    rotation_matrix = np.eye(4)
    rotation_matrix[:3, :3] = obb.R
    pv_obb.transform(rotation_matrix, inplace=True)
    pv_obb.scale(obb.extent, inplace=True)
    pv_obb.translate(obb.center, inplace=True)
    
    # Create the ROI box mesh
    roi_box_mesh = pv.Box(bounds=(*roi_bbox.min_bound, *roi_bbox.max_bound))

    # Add meshes to the scene
    plotter.add_mesh(roi_box_mesh, style='wireframe', line_width=2, color='yellow', label='Region of Interest (ROI)')
    plotter.add_mesh(pv_plane, color='blue', point_size=3, render_points_as_spheres=True, label='Detected Plane')
    plotter.add_mesh(pv_object, color='lightgreen', point_size=5, render_points_as_spheres=True, label='Isolated Object')
    plotter.add_mesh(pv_obb, style='wireframe', line_width=5, color='red', label='Bounding Box')
    
    # Add text with the measurements
    length = measurements['length']
    width = measurements['width']
    area = measurements['area']
    plotter.add_text(f"Length: {length:.1f} mm\nWidth: {width:.1f} mm\nArea: {area/100:.1f} cm^2", 
                     position='upper_left', font_size=12, color='white')
    
    plotter.add_legend()
    plotter.show_axes()
    plotter.show()