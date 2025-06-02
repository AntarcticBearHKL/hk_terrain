import numpy as np
import cv2

def empty_heightmap(size):
    return [[0 for x in range(size)] for y in range(size)]

def gaussian_blur(heightmap, blur_radius):
    if blur_radius <= 0:
        return heightmap
    
    if blur_radius % 2 == 0:
        blur_radius += 1
    
    size = len(heightmap)
    image = np.zeros((size, size), dtype=np.float32)
    
    # 将 heightmap 转换为 numpy 数组
    for y in range(size):
        for x in range(size):
            image[y][x] = heightmap[y][x]
    
    # 进行高斯模糊
    blurred_image = cv2.GaussianBlur(image, (blur_radius, blur_radius), 0)
    
    # 将模糊结果直接写回原始 heightmap
    for y in range(size):
        for x in range(size):
            heightmap[y][x] = blurred_image[y][x]

def render_heightmap(heightmap):
    size = len(heightmap)
    image = np.zeros((size, size), dtype=np.uint16)

    for y in range(size):
        for x in range(size):
            image[y][x] = int(heightmap[y][x] * 65536)

    cv2.imwrite('terrain_raw.png', image)
    
    return image

def show_img(image):
    cv2.imshow('Terrain', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()