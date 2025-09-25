import time
import numpy as np
import freenect
import pyvista as pv  # Substitui Matplotlib

# ==== Parâmetros intrínsecos do Kinect v1 (aprox) ====
FX = 594.21
FY = 591.04
CX = 339.5
CY = 242.7

# ==== Ajustes de visualização/performance ====
STEP = 4          # downsample por passo de pixels (4 => ~160x120 pontos)
Z_MIN = 500.0     # mm (corta muito perto)
Z_MAX = 4000.0    # mm (corta muito longe)
MAX_POINTS = 40000 # limite de pontos no scatter (por segurança)

# As funções de captura e conversão de dados permanecem as mesmas
def get_depth_mm():
    """Captura um frame de profundidade em milímetros (float32)."""
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    if depth is None:
        raise RuntimeError("Não foi possível ler profundidade do Kinect.")
    return depth.astype(np.float32)

def depth_to_points_xyz(depth_mm, step=4, zmin=500.0, zmax=4000.0):
    """Converte mapa de profundidade para pontos 3D (XYZ) com downsample."""
    d = depth_mm[::step, ::step]
    h, w = d.shape
    i, j = np.meshgrid(np.arange(w, dtype=np.float32),
                       np.arange(h, dtype=np.float32),
                       indexing='xy')
    z = d
    x = (i*step - CX) * z / FX
    y = (j*step - CY) * z / FY
    mask = (z > 0) & np.isfinite(z) & (z >= zmin) & (z <= zmax)
    x, y, z = x[mask], y[mask], z[mask]
    pts = np.stack((x, y, z), axis=-1)
    if pts.shape[0] > MAX_POINTS:
        idx = np.random.choice(pts.shape[0], size=MAX_POINTS, replace=False)
        pts = pts[idx]
    return pts

# A função set_axes_equal não é mais necessária, PyVista cuida disso.

def main():
    print("Iniciando visualização ao vivo com PyVista... Pressione 'q' na janela para encerrar.")

    # --- Configuração inicial do PyVista ---
    plotter = pv.Plotter(window_size=[1024, 768])

    # Captura o primeiro frame para inicializar a nuvem de pontos
    try:
        depth0 = get_depth_mm()
        pts0 = depth_to_points_xyz(depth0, step=STEP, zmin=Z_MIN, zmax=Z_MAX)
        if pts0.size == 0:
            raise RuntimeError("Nenhum ponto válido no primeiro frame. Ajuste Z_MIN/Z_MAX.")
    except RuntimeError as e:
        print(f"Erro: {e}")
        return

    # Cria o objeto de malha (nuvem de pontos) do PyVista
    # Usamos pv.PolyData para representar a nuvem de pontos
    point_cloud = pv.PolyData(pts0)
    
    # Adiciona a malha ao plotter. 'render_points_as_spheres=False' é mais rápido
    # O nome 'kinect_cloud' é um identificador que podemos usar depois se precisarmos
    plotter.add_mesh(point_cloud,
                     style='points',
                     color='cyan',
                     point_size=2,
                     render_points_as_spheres=False,
                     name='kinect_cloud')

    # Configura a cena
    plotter.add_axes()
    plotter.show_grid(color='#222222')
    plotter.set_background('black')
    
    # Inicia a visualização em modo interativo e não-bloqueante
    plotter.show(interactive_update=True, auto_close=False)

    print("Visualizador iniciado. Loop principal rodando...")
    try:
        while plotter.close:
            # Captura novos dados de profundidade
            depth = get_depth_mm()
            pts = depth_to_points_xyz(depth, step=STEP, zmin=Z_MIN, zmax=Z_MAX)

            if pts.size == 0:
                # Se não houver pontos, podemos limpar a malha ou pular o frame
                point_cloud.points = np.zeros((0, 3)) # Limpa os pontos
            else:
                # --- A MÁGICA ACONTECE AQUI ---
                # Atualiza as coordenadas dos pontos na malha existente
                point_cloud.points = pts
                # Força uma atualização dos limites da câmera para se ajustar aos novos pontos
                plotter.camera.reset_clipping_range()

            # Renderiza a cena atualizada e processa eventos da janela (ex: fechar, mover)
            plotter.update()

    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário (Ctrl+C).")
    finally:
        # Garante que a janela seja fechada ao sair
        plotter.close()
        print("Visualizador fechado.")


if __name__ == "__main__":
    main()