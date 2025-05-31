import cv2
import numpy as np
from noise import pnoise2

from hydraulic_erosion import HydraulicErosion

size = 512

width, height = size, size
scale = size
octaves = 6
persistence = 0.5
lacunarity = 2.0
base = 42

rgb_image = np.zeros((height, width), dtype=np.uint16)
heightmap = [[0 for x in range(width)] for y in range(height)]

for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale
        noise_val = pnoise2(nx, ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=base)
        pixel_value = (noise_val + 1) / 2
        heightmap[y][x] = pixel_value

erosion_simulator = HydraulicErosion(heightmap)
erosion_simulator.simulate(70000)

for y in range(height):
    for x in range(width):
        rgb_image[y][x] = int( heightmap[y][x] * 65536)- 1000

rgb_image = cv2.GaussianBlur(rgb_image, (15, 15), 0)
cv2.imwrite('D:\\terrain_raw.png', rgb_image)