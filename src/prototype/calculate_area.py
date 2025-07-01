from svgpathtools import svg2paths
import re
import argparse

parser = argparse.ArgumentParser(description="Calculo de area interna")
parser.add_argument('svg_input', type=str, help='svg file')

args = parser.parse_args()

def polygon_area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1)%n]
        area += (x1 * y2) - (x2 * y1)
    return abs(area) / 2.0

def extract_points_from_path(path_string):
    # Extrai todos os pares de números float do path
    numbers = [float(num) for num in re.findall(r'[-+]?[0-9]*\.?[0-9]+', path_string)]
    # Agrupa em pares (x, y)
    points = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
    return points

# Carregar paths do SVG
paths, attributes = svg2paths(args.svg_input)

total_area = 0
for i, attr in enumerate(attributes):
    d = attr.get('d')
    if not d:
        continue
    points = extract_points_from_path(d)
    if len(points) < 3:
        continue  # ignora linhas ou pontos
    area = polygon_area(points)
    total_area += area
    print(f"Contorno {i+1}: área = {area:.2f} unidades²")

print(f"Área total aproximada: {total_area:.2f} unidades²")
