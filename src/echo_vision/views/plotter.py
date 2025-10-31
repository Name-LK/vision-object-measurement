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

def display_live_results(capturer):
    """Cria e exibe a cena 3D em tempo real com PyVista."""
    print("Iniciando visualização ao vivo com PyVista... Pressione 'q' na janela para encerrar.")

    # --- Configuração inicial do PyVista ---
    plotter = pv.Plotter(window_size=[1280, 720])

    # Captura o primeiro frame para inicializar a nuvem de pontos
    initial_pcd = capturer.get_point_cloud()
    if initial_pcd is None or initial_pcd.is_empty():
        print("Erro: Nenhum ponto válido no primeiro frame. Verifique a conexão ou os parâmetros.")
        return

    # Cria o objeto de malha (nuvem de pontos) do PyVista
    point_cloud_mesh = pv.PolyData(np.asarray(initial_pcd.points))

    # Adiciona a malha ao plotter com um nome para referência futura
    plotter.add_mesh(point_cloud_mesh,
                     style='points',
                     color='cyan',
                     point_size=2,
                     render_points_as_spheres=False,
                     name='kinect_cloud')

    # Configura a cena
    plotter.add_axes()
    plotter.set_background('black')
    plotter.show_grid(color='#333333')

    # Inicia a visualização em modo interativo e não-bloqueante
    plotter.show(interactive_update=True, auto_close=False)
    print("Visualizador iniciado. Loop principal rodando...")

    try:
        # Loop principal de atualização
        while plotter.close:
            # Captura uma nova nuvem de pontos
            pcd = capturer.get_point_cloud()

            if pcd is None or pcd.is_empty():
                point_cloud_mesh.points = np.zeros((0, 3)) # Limpa a malha se a captura falhar
            else:
                # A MÁGICA ACONTECE AQUI: atualiza os pontos da malha existente
                point_cloud_mesh.points = np.asarray(pcd.points)
                plotter.camera.reset_clipping_range() # Ajusta a câmera

            # Renderiza a cena atualizada e processa eventos da janela
            plotter.update()

    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário (Ctrl+C).")
    finally:
        # Garante que a janela seja fechada ao sair
        plotter.close()
        print("Visualizador fechado.")

def display_live_rgb_capture(capturer):
    print("Setting up PyVista Pllotter...")
    plotter = pv.Plotter()

    #Catch a initial frame
    try:
        rgb_frame = capturer.get_rgb_video()
    except TypeError:
        print("\n[ERROR] Can't get a kinect RGB frame")
        exit()
    
    height, width, _ = rgb_frame.shape 

    #Create the texture using initial frame
    tex = pv.Texture(rgb_frame)

    #Create a 2D plan
    plane = pv.Plane(center=(width/2, height/2, 0),
                     i_size=width,
                     j_size=height)
    
    actor = plotter.add_mesh(plane, texture=tex)

    #Config the camera
    plotter.view_xy()
    plotter.enable_parallel_projection()

    print("Starting 2D loop...")

    plotter.show(interactive_update=True, auto_close=False)

    #Main loop to get the next frame
    while not plotter._closed:
        new_rgb_frame = capturer.get_rgb_video()
        actor.texture = pv.Texture(new_rgb_frame)

        #Update the plotter
        plotter.update()
    
    #Cleaning
    print("Closing plotter")
    plotter.close()