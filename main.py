import lib.terrain as terrain
import lib.perlin_noise
from lib.hydraulic_erosion import HydraulicErosion
import math

heightmap = terrain.empty_heightmap(512)

lib.perlin_noise.apply(heightmap, weight=1, octaves=8, persistence=0.3, lacunarity=2, rotation_angle=math.pi / 4, non_roughness=1.75)

HydraulicErosion(heightmap, inertia=0.9, capacity=1024, deposition=0.1, erosion=0.1, evaporation=0.02, min_slope=0.1, gravity=10, radius=64, max_path=128).simulate(10000)

terrain.gaussian_blur(heightmap, blur_radius=16)
terrain.render_heightmap(heightmap)