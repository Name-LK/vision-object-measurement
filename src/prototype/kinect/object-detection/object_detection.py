#run the RGB live pipeline and detect objects by color

from echo_vision.logic.rgb_capture import rgb_live_pipeline
from echo_vision.processing.frame.rgb_frame import get_frame
from echo_vision.capture.factory import SensorFactory
from echo_vision.utils.config_loader import load_config

import cv2
import numpy as np

lower_color = np.array([100, 150, 50])
upper_color = np.array([130, 255, 255])

config = load_config('config.yaml')
sensor_type = config.get('sensor', {}).get('type', 'kinect_v1')
capturer = SensorFactory.create_capturer(sensor_type=sensor_type, config=config)

print("Iniciando loop de processamento... Pressione 'q' para sair.")

while True:
    # 1. Ler o frame (agora da sua função do Kinect)
    frame = get_frame(capturer)

    # Verificar se o frame foi capturado com sucesso
    if frame is None:
        print("Erro: Não foi possível ler o frame do Kinect.")
        break

    # O RESTO DO SCRIPT É EXATAMENTE O MESMO
    
    # 2. Converter de BGR para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 3. Criar a máscara de cor
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # 4. Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 5. Processar o maior contorno (se houver algum)
    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 500:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Objeto Detectado", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 6. Exibir os resultados
    cv2.imshow("Frame Kinect (Processado)", frame)
    cv2.imshow("Mascara (Cor Detectada)", mask)

    # Parar o loop ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# NÃO PRECISAMOS MAIS DESTA LINHA:
# cap.release()

cv2.destroyAllWindows()