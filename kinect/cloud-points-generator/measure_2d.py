import numpy as np
import freenect
import open3d as o3d
import pyvista as pv

# --- Mantenha as mesmas funções de captura e conversão ---
FX, FY, CX, CY = 594.21, 591.04, 339.5, 242.7

def get_depth_mm():
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    if depth is None:
        raise RuntimeError("Não foi possível ler profundidade do Kinect.")
    return depth.astype(np.float32)

def depth_to_points_xyz(depth_mm):
    # Usando step=1 para máxima resolução no objeto
    d = depth_mm[::1, ::1]
    h, w = d.shape
    i, j = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32), indexing='xy')
    z = d
    x = (i - CX) * z / FX
    y = (j - CY) * z / FY
    mask = (z > 850.0) & (z < 2000.0) # Foco em uma faixa de distância mais próxima
    x, y, z = x[mask], y[mask], z[mask]
    return np.stack((x, y, z), axis=-1)

def main():
    print("Capturando um frame do Kinect para análise...")
    try:
        depth = get_depth_mm()
        pts = depth_to_points_xyz(depth)
    except RuntimeError as e:
        print(f"Erro: {e}")
        return

    # 1. Converter nuvem de pontos NumPy para o formato Open3D
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    print(f"Nuvem de pontos original com {len(pcd.points)} pontos.")

    # 2. Pré-processamento: Isolar a área de interesse (ROI)
    # Vamos assumir que o objeto está mais ou menos no centro
    # bbox = o3d.geometry.AxisAlignedBoundingBox(min_bound=(-250, -250, 850), max_bound=(250, 250, 1500))
    # pcd = pcd.crop(bbox)
    # print(f"Pontos após o corte (ROI): {len(pcd.points)}.")


    # 3. Detectar o plano (mesa) usando RANSAC
    # distance_threshold: quão perto um ponto deve estar do plano para ser considerado parte dele
    # ransac_n: quantos pontos são amostrados para estimar um plano
    # num_iterations: quantas vezes o algoritmo roda
    plane_model, inliers = pcd.segment_plane(distance_threshold=5.0, ransac_n=3, num_iterations=1000)
    
    # [a, b, c, d] são os coeficientes do plano ax + by + cz + d = 0
    a, b, c, d = plane_model
    print(f"Equação do plano detectado: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    # Separar os pontos: inliers são o plano, outliers são o resto (nosso objeto)
    plane_cloud = pcd.select_by_index(inliers)
    object_cloud = pcd.select_by_index(inliers, invert=True)

    # Remover ruídos do objeto isolado
    object_cloud = object_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)[0]
    print(f"Pontos do objeto isolado: {len(object_cloud.points)}.")


    # 4. Calcular a Caixa Delimitadora Orientada (Oriented Bounding Box - OBB)
    # Esta caixa se ajusta à rotação do objeto para dar o comprimento e largura reais
    obb = object_cloud.get_oriented_bounding_box()
    obb.color = (1, 0, 0) # Cor vermelha
    
    # As dimensões da caixa
    dims = obb.extent
    length = max(dims)
    width = sorted(dims)[1] # O segundo maior valor
    height = min(dims) # A menor dimensão geralmente é a altura, mas pode variar

    print("\n--- Medições 2D ---")
    print(f"Comprimento: {length:.1f} mm")
    print(f"Largura:     {width:.1f} mm")


    # 5. Calcular a Área da Base (usando o Casco Convexo 2D)
    # Projetar os pontos do objeto no plano XY (ignorando Z)
    object_points_2d = np.asarray(object_cloud.points)[:, :2]
    
    # Criar uma nuvem de pontos 2D (mas em formato 3D com Z=0 para usar as funções do Open3D)
    pcd_2d = o3d.geometry.PointCloud()
    pcd_2d.points = o3d.utility.Vector3dVector(np.hstack([object_points_2d, np.zeros((object_points_2d.shape[0], 1))]))
    
    # Calcular o casco convexo (convex hull) da projeção 2D
    hull, _ = pcd_2d.compute_convex_hull()
    area = hull.get_area() # A "área" de uma malha 2D é a área do polígono

    print(f"Área da Base (estimada): {area / 100:.1f} cm²\n") # Convertendo mm² para cm²


    # 6. Visualizar tudo com PyVista
    plotter = pv.Plotter(window_size=[1280, 720])
    plotter.set_background('black')
    
    # Converter geometria do Open3D para PyVista
    pv_plane = pv.PolyData(np.asarray(plane_cloud.points))
    pv_object = pv.PolyData(np.asarray(object_cloud.points))
    pv_obb = pv.wrap(obb)

    plotter.add_mesh(pv_plane, color='blue', point_size=3, render_points_as_spheres=True, label='Plano Detectado')
    plotter.add_mesh(pv_object, color='lightgreen', point_size=5, render_points_as_spheres=True, label='Objeto Isolado')
    plotter.add_mesh(pv_obb, style='wireframe', line_width=5, color='red', label='Caixa Delimitadora')

    # Adicionar texto com as medidas na tela
    plotter.add_text(f"Comprimento: {length:.1f} mm\nLargura: {width:.1f} mm\nArea: {area/100:.1f} cm^2", 
                     position='upper_left', font_size=12, color='white')
    
    plotter.add_legend()
    plotter.show_axes()
    plotter.show()


if __name__ == "__main__":
    main()