import freenect
import pyvista as pv
import numpy as np

def get_video_rgb():
    """Obtém o frame de vídeo (RGB) do Kinect."""
    array, _ = freenect.sync_get_video()
    return array

# --- Configuração do PyVista ---
print("Configurando o plotter do PyVista...")

plotter = pv.Plotter()

# Pega um frame inicial
try:
    frame_rgb = get_video_rgb()
except TypeError:
    print("\n[ERRO] Não foi possível obter o frame do Kinect.")
    print("Verifique se o Kinect v1 (modelo Xbox 360) está conectado.")
    print("Pode ser necessário rodar o script com 'sudo' (ex: sudo python seu_script.py)\n")
    exit()
    
height, width, _ = frame_rgb.shape

# Cria a textura do PyVista com o frame inicial
tex = pv.Texture(frame_rgb)

# Cria um plano 2D
plane = pv.Plane(center=(width/2, height/2, 0), 
                 i_size=width, 
                 j_size=height)

# --- MUDANÇA 1: Salve o 'actor' ---
# plotter.add_mesh() retorna o ator. Precisamos dele.
actor = plotter.add_mesh(plane, texture=tex)

# Configura a câmera
plotter.view_xy()
plotter.enable_parallel_projection() 

print("Iniciando o loop 2D... Pressione 'q' na janela para sair.")

plotter.show(interactive_update=True, auto_close=False)

# Loop principal
while not plotter._closed:
    
    # 1. Obter novo frame RGB
    frame_rgb_new = get_video_rgb()
    
    # --- MUDANÇA 2: Crie uma nova textura e atribua ao ator ---
    # Em vez de 'tex.image = ...', criamos uma nova textura
    # e a atribuímos à propriedade '.texture' do ator.
    actor.texture = pv.Texture(frame_rgb_new)
    
    # 3. Atualizar o plotter
    plotter.update()

# --- Limpeza ---
print("Fechando...")
plotter.close()
freenect.sync_stop()