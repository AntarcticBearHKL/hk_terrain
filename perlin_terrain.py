import cv2
import numpy as np
from noise import pnoise2

from hydraulic_erosion import HydraulicErosion

width, height = 512, 512
scale = 512
octaves = 6
persistence = 0.5
lacunarity = 2.0
base = 42

rgb_image = np.zeros((height, width), dtype=np.uint16)

for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale
        noise_val = pnoise2(nx, ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=base)
        pixel_value = int((noise_val + 1) * 32767.5)
        rgb_image[y][x] = pixel_value

erosion_simulator = HydraulicErosion(rgb_image)
eroded_heightmap = erosion_simulator.simulate(300000)

cv2.imwrite('D:\\terrain_raw.png', eroded_heightmap)