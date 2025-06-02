from noise import pnoise2
from random import randint, uniform
import logging
import math

def apply(
            heightmap, 
            weight=1.0, 
            octaves=3, 
            persistence=0.5, 
            lacunarity=2.0,
            non_roughness=1.0,
            rotation_angle=None
    ):
    """
    Apply Perlin noise to a heightmap.
    
    Parameters:
        heightmap (list): 2D list of height values
        weight (float): Blend weight between original heightmap and noise (0.0-1.0)
        octaves (int): Number of octaves for noise generation
        persistence (float): Persistence value for noise
        lacunarity (float): Lacunarity value for noise
        base (int): Seed for noise generation, random if None
        rotation_angle (float): Angle for noise rotation in radians, random if None
        roughness (float): Roughness factor for the noise     
    """
    try:
        if not heightmap:
            raise ValueError("Heightmap cannot be empty")
        
        height = len(heightmap)
        if height == 0:
            raise ValueError("Heightmap height cannot be zero")
            
        width = len(heightmap[0])
        if width == 0:
            raise ValueError("Heightmap width cannot be zero")
        
        if any(len(row) != width for row in heightmap):
            raise ValueError("All rows in heightmap must have the same length")
        
        # Use default random values if not provided
        base = randint(0, 1000)
        rotation_angle = rotation_angle if rotation_angle is not None else uniform(0, math.pi * 2)
        
        # 确保权重在0-1范围内
        weight = max(0.0, min(1.0, weight))
        
        scale = max(width, height) * non_roughness
        
        # 计算旋转变换的正弦和余弦值
        cos_rot = math.cos(rotation_angle)
        sin_rot = math.sin(rotation_angle)
        
        for y in range(height):
            for x in range(width):
                # 标准化坐标
                nx = x / scale
                ny = y / scale
                
                # 应用旋转变换
                rx = nx * cos_rot - ny * sin_rot
                ry = nx * sin_rot + ny * cos_rot
                
                # 使用旋转后的坐标生成噪声
                noise_val = pnoise2(rx+base, ry+base, 
                                  octaves=octaves, 
                                  persistence=persistence, 
                                  lacunarity=lacunarity, 
                                  base=base)

                # 将噪声值规范化到0-1范围
                normalized_noise = (noise_val + 1) / 2
                
                # 按权重混合噪声和原始高度值
                heightmap[y][x] = heightmap[y][x] * (1 - weight) + normalized_noise * weight
        
    except Exception as e:
        logging.error(f"Error in apply_perlin_noise: {e}")
        raise