import time
import numpy as np
import freenect
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (necessário para proj 3D)

# ==== Parâmetros intrínsecos do Kinect v1 (aprox) ====
FX = 594.21
FY = 591.04
CX = 339.5
CY = 242.7

# ==== Ajustes de visualização/performance ====
STEP = 4           # downsample por passo de pixels (4 => ~160x120 pontos)
Z_MIN = 500.0      # mm (corta muito perto)
Z_MAX = 4000.0     # mm (corta muito longe)
MAX_POINTS = 40000 # limite de pontos no scatter (por segurança)
FPS_LIMIT = 10     # taxa-alvo de atualização (frames por segundo)

def get_depth_mm():
    """Captura um frame de profundidade em milímetros (float32)."""
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    if depth is None:
        raise RuntimeError("Não foi possível ler profundidade do Kinect.")
    return depth.astype(np.float32)

def depth_to_points_xyz(depth_mm, step=4, zmin=500.0, zmax=4000.0):
    """Converte mapa de profundidade para pontos 3D (XYZ) com downsample."""
    # Amostragem por passo para acelerar
    d = depth_mm[::step, ::step]

    h, w = d.shape
    i, j = np.meshgrid(np.arange(w, dtype=np.float32),
                       np.arange(h, dtype=np.float32),
                       indexing='xy')

    z = d
    x = (i*step - CX) * z / FX
    y = (j*step - CY) * z / FY

    # Máscara: remove zeros/NaN e corta por faixa
    mask = (z > 0) & np.isfinite(z) & (z >= zmin) & (z <= zmax)

    x = x[mask]
    y = y[mask]
    z = z[mask]

    pts = np.stack((x, y, z), axis=-1)

    # Se ainda tem muitos pontos, amostra aleatoriamente
    if pts.shape[0] > MAX_POINTS:
        idx = np.random.choice(pts.shape[0], size=MAX_POINTS, replace=False)
        pts = pts[idx]

    return pts

def set_axes_equal(ax):
    """Deixa os eixos com mesma escala (importante p/ 3D ficar proporcional)."""
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    max_range = max([x_range, y_range, z_range])
    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    ax.set_xlim3d([x_middle - max_range/2, x_middle + max_range/2])
    ax.set_ylim3d([y_middle - max_range/2, y_middle + max_range/2])
    ax.set_zlim3d([z_middle - max_range/2, z_middle + max_range/2])

def main():
    print("Iniciando visualização ao vivo... Pressione Ctrl+C para encerrar.")
    # Primeiro frame para dimensionar
    depth0 = get_depth_mm()
    pts0 = depth_to_points_xyz(depth0, step=STEP, zmin=Z_MIN, zmax=Z_MAX)
    if pts0.size == 0:
        raise RuntimeError("Nenhum ponto válido no primeiro frame. Ajuste Z_MIN/Z_MAX.")

    # Figura e eixos 3D
    plt.ion()
    fig = plt.figure("Kinect 3D Live")
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(pts0[:, 0], pts0[:, 1], pts0[:, 2], s=1, depthshade=False)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title("Kinect - Nuvem de Pontos (ao vivo)")

    # Limites iniciais razoáveis a partir do primeiro frame
    margin = 200.0
    ax.set_xlim(pts0[:, 0].min()-margin, pts0[:, 0].max()+margin)
    ax.set_ylim(pts0[:, 1].min()-margin, pts0[:, 1].max()+margin)
    ax.set_zlim(pts0[:, 2].min()-margin, pts0[:, 2].max()+margin)
    set_axes_equal(ax)

    last = time.time()
    target_dt = 1.0 / max(1, FPS_LIMIT)

    try:
        while True:
            # Controle simples de FPS
            now = time.time()
            if now - last < target_dt:
                time.sleep(target_dt - (now - last))
            last = time.time()

            depth = get_depth_mm()
            pts = depth_to_points_xyz(depth, step=STEP, zmin=Z_MIN, zmax=Z_MAX)
            if pts.size == 0:
                continue

            # Atualiza dados do scatter (truque para 3D)
            sc._offsets3d = (pts[:, 0], pts[:, 1], pts[:, 2])

            # Atualiza limites de forma suave (opcional)
            # Comentado por estabilidade; descomente se quiser autoscale:
            # ax.set_xlim(pts[:, 0].min()-margin, pts[:, 0].max()+margin)
            # ax.set_ylim(pts[:, 1].min()-margin, pts[:, 1].max()+margin)
            # ax.set_zlim(pts[:, 2].min()-margin, pts[:, 2].max()+margin)
            # set_axes_equal(ax)

            plt.draw()
            plt.pause(0.001)

    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
    finally:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()

