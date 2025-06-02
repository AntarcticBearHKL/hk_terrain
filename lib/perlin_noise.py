from noise import pnoise2
from random import randint

class PerlinNoise:
    def __init__(self, octaves=3, persistence=0.5, lacunarity=2.0, base=None):
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.base = base if base is not None else randint(0, 100000)
    
    def apply(self, heightmap: list[list], scale_factor=1):
        height = len(heightmap)
        width = len(heightmap[0]) if height > 0 else 0
        scale = max(width, height) * scale_factor
        
        for y in range(height):
            for x in range(width):
                nx = x / scale
                ny = y / scale
                noise_val = pnoise2(nx, ny, 
                                   octaves=self.octaves, 
                                   persistence=self.persistence, 
                                   lacunarity=self.lacunarity, 
                                   base=self.base)

                heightmap[y][x] = (noise_val + 1) / 2