import torch
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Detecção do contorno e exportação em SVG")
parser.add_argument('image', type=str, help='Processed image input')
parser.add_argument('-o', type=str,default='output', help='Name of the output file')

args = parser.parse_args()

# Para salvar o SVG
def contours_to_svg(contours, width, height, svg_filename):
    with open(svg_filename, 'w') as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
        for contour in contours:
            if len(contour) < 2:
                continue
            path_data = "M " + " L ".join(f"{point[0][0]} {point[0][1]}" for point in contour) + " Z"
            f.write(f'  <path d="{path_data}" stroke="black" fill="none"/>\n')
        f.write('</svg>')

# Carregar YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)



# Carregar imagem
image_path = args.image  # troque pelo caminho da sua imagem
img = cv2.imread(image_path)
height, width = img.shape[:2]
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Detectar objetos
results = model(img_rgb)
df = results.pandas().xyxy[0]

all_contours = []

for index, row in df.iterrows():
    x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
    roi = img[y1:y2, x1:x2]

    # Converter para cinza e detectar bordas
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Ajustar coordenadas do contorno para posição na imagem original
    for contour in contours:
        contour += [x1, y1]  # desloca pontos do ROI para posição global
    all_contours.extend(contours)

# Salvar como SVG
contours_to_svg(all_contours, width, height, f"{args.o}.svg")
print("SVG salvo como output.svg!")
