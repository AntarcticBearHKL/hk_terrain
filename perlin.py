import cv2
import numpy as np
from noise import pnoise2

width, height = 512, 512
scale = 450
octaves = 6        # 增加细节层数
persistence = 0.5  # 控制细节的明显程度
lacunarity = 2.0   # 控制频率变化
base = 42          # 随机种子

# 将数组类型更改为uint16
rgb_image = np.zeros((height, width), dtype=np.uint16)

for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale
        # 使用更多参数获取更丰富的噪声
        noise_val = pnoise2(nx, ny, 
                          octaves=octaves, 
                          persistence=persistence, 
                          lacunarity=lacunarity, 
                          base=base)
        # 将-1到1的值转换为0到65535
        pixel_value = int((noise_val + 1) * 32767.5)
        rgb_image[y][x] = pixel_value

# 对生成的灰度图应用高斯模糊
# 参数: 源图像, 高斯核大小(必须是奇数), X和Y方向的标准差
blurred_image = cv2.GaussianBlur(rgb_image, (15, 15), 0)

# 显示原始图像 (注意: 显示16位图像可能需要归一化)
cv2.imshow('Original Perlin Noise Image', (rgb_image / 256).astype(np.uint8))
# 显示模糊后的图像
cv2.imshow('Blurred Perlin Noise Image', (blurred_image / 256).astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存原始图像 (16位png)
cv2.imwrite('D:\\perlin_noise_16bit.png', rgb_image)
# 保存模糊后的图像 (16位png)
cv2.imwrite('D:\\perlin_noise_blurred_16bit.png', blurred_image)