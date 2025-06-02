import numpy as np
import cv2

class Terrain:
    def __init__(self, size):
        self.size = size
        self.image = np.zeros((self.size, self.size), dtype=np.uint16)
        self.heightmap = [[0 for x in range(self.size)] for y in range(self.size)]

    def get_heightmap(self):
        return self.heightmap

    def render(self):
        for y in range(self.size):
            for x in range(self.size):
                self.image[y][x] = int(self.heightmap[y][x] * 65536)

        cv2.imwrite('terrain_raw.png', self.image)

    def show_img(self):
        cv2.imshow('Terrain', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()