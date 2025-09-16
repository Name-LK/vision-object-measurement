import freenect
import cv2
import numpy as np

print("Pressione 'Esc' para sair.")

def get_video():
    # Obtém um frame de vídeo RGB do Kinect
    # Retorna uma imagem numpy 640x480x3 RGB
    array, _ = freenect.sync_get_video()
    return array

def get_depth():
    # Obtém um frame de profundidade do Kinect
    # Retorna uma imagem numpy 640x480
    array, _ = freenect.sync_get_depth()
    # A profundidade bruta é 11-bit. Normalizamos para 8-bit para visualização.
    # Podemos mapear os valores de 0-2047 para 0-255
    normalized_depth = (array / 8).astype(np.uint8)
    return normalized_depth

if __name__ == "__main__":
    try:
        while True:
            # Obtém e exibe o stream de vídeo colorido
            video_frame = get_video()
            cv2.imshow('Kinect RGB', cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR))

            # Obtém e exibe o stream de profundidade
            depth_frame = get_depth()
            cv2.imshow('Kinect Profundidade', depth_frame)

            # Verifica se a tecla 'Esc' foi pressionada
            key = cv2.waitKey(1) & 0xFF
            if key == 27: # 27 é o código ASCII para 'Esc'
                break

    except freenect.FreenectError as e:
        print(f"Erro ao inicializar ou acessar o Kinect: {e}")
        print("Verifique se o Kinect está conectado e as regras udev estão configuradas corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        cv2.destroyAllWindows()
        print("Teste finalizado.")