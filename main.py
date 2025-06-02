from lib.terrain import Terrain
from lib.perlin_noise import PerlinNoise

terrain = Terrain(512)
PerlinNoise(5, 0.5, 16).apply(terrain.get_heightmap())
terrain.render()