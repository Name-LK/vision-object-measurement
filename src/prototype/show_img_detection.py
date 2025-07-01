import torch
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Calculo de area interna")
parser.add_argument('input', type=str, help='image file')

args = parser.parse_args()

# Carregar YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Ler imagem
image_path = args.input
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Detectar objetos
results = model(img_rgb)
df = results.pandas().xyxy[0]

for index, row in df.iterrows():
    x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
    
    # Recortar a ROI (região do objeto)
    roi = img[y1:y2, x1:x2]
    
    # Converter para cinza e aplicar Canny
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Desenhar contornos na imagem original
    cv2.drawContours(img[y1:y2, x1:x2], contours, -1, (0,255,0), 2)

# Mostrar o resultado
cv2.imshow("Silhueta do Objeto", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
