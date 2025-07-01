import cv2
import torch

# Iniciar webcam com alta resolução e tentar FPS alto
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Carregar modelo
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO espera RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Rodar o modelo
    results = model(frame_rgb, size=640)  # diminui size p/ ser mais rápido
    annotated_frame = results.render()[0]

    cv2.imshow('YOLO Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
