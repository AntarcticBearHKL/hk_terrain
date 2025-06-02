import math
import random

class HydraulicErosion:
    def __init__(self, heightmap, inertia=0.01, capacity=32, deposition=0.1, erosion=0.9, evaporation=0.02, min_slope=0.01, gravity=10, radius=32, max_path=64):
        """
        初始化水力侵蚀模拟类。
        :param heightmap: 地形高度图，list[list]格式
        :param inertia: 惯性参数，取值范围0-1
        :param capacity: 携带能力参数
        :param deposition: 沉积速度参数，取值范围0-1
        :param erosion: 侵蚀速度参数，取值范围0-1
        :param evaporation: 蒸发速度参数，取值范围0-1
        :param min_slope: 最小坡度参数
        :param gravity: 重力参数
        :param radius: 侵蚀半径
        :param max_path: 粒子最大移动步数
        """

        self.heightmap = heightmap
        self.inertia = inertia
        self.capacity = capacity
        self.deposition = deposition
        self.erosion = erosion
        self.evaporation = evaporation
        self.min_slope = min_slope
        self.gravity = gravity
        self.radius = radius
        self.max_path = max_path
        self.heightmap_height = len(heightmap)
        self.heightmap_width = len(heightmap[0])

    def interpolate_gradient(self, pos):
        """
        计算粒子当前位置的梯度。
        :param pos: 粒子位置，二维坐标 (x, y)
        :return: 梯度向量 [gx, gy]
        """

        x, y = pos
        # 确保粒子在有效范围内
        x = max(0, min(x, self.heightmap_width - 1.001))
        y = max(0, min(y, self.heightmap_height - 1.001))
        
        x_floor, y_floor = int(x), int(y)
        # 确保索引不会越界
        x_next = min(x_floor + 1, self.heightmap_width - 1)
        y_next = min(y_floor + 1, self.heightmap_height - 1)
        
        u, v = x - x_floor, y - y_floor
        
        # 使用list索引方式访问高度值，注意list是[y][x]格式
        h00 = float(self.heightmap[y_floor][x_floor])
        h10 = float(self.heightmap[y_floor][x_next])
        h01 = float(self.heightmap[y_next][x_floor])
        h11 = float(self.heightmap[y_next][x_next])
        
        # 使用浮点数计算差值，避免溢出
        gx1 = h10 - h00
        gx2 = h11 - h01
        gy1 = h01 - h00
        gy2 = h11 - h10
        
        gx = gx1 * (1 - v) + gx2 * v
        gy = gy1 * (1 - u) + gy2 * u
        return [gx, gy]

    def vector_norm(self, vector):
        """计算向量的模长"""
        return math.sqrt(vector[0]**2 + vector[1]**2)
    
    def vector_normalize(self, vector):
        """归一化向量"""
        norm = self.vector_norm(vector)
        if norm == 0:
            return [random.uniform(-1, 1), random.uniform(-1, 1)]
        return [vector[0]/norm, vector[1]/norm]
    
    def vector_add(self, v1, v2):
        """向量加法"""
        return [v1[0] + v2[0], v1[1] + v2[1]]
    
    def vector_multiply(self, vector, scalar):
        """向量乘以标量"""
        return [vector[0] * scalar, vector[1] * scalar]
    
    def update_drop(self, drop):
        """
        更新粒子的状态，包括位置、速度、携带的沉积物等。
        :param drop: 粒子信息，字典包含 'pos', 'dir','vel', 'water','sediment'
        :return: 更新后的粒子信息
        """

        pos = drop['pos']
        old_dir = drop['dir']

        gradient = self.interpolate_gradient(pos)
        
        # 使用自定义向量操作代替numpy
        inertia_component = self.vector_multiply(old_dir, self.inertia)
        gradient_component = self.vector_multiply(gradient, -(1 - self.inertia))
        new_dir = self.vector_add(inertia_component, gradient_component)
        new_dir = self.vector_normalize(new_dir)
        
        new_pos = self.vector_add(pos, new_dir)
        
        # 检查是否越界
        if (new_pos[0] < 0 or new_pos[0] >= self.heightmap_width or 
            new_pos[1] < 0 or new_pos[1] >= self.heightmap_height):
            return None
        
        # 注意heightmap的访问顺序是[y][x]
        h_new = float(self.heightmap[int(new_pos[1])][int(new_pos[0])])
        h_old = float(self.heightmap[int(pos[1])][int(pos[0])])
        h_dif = h_new - h_old
        
        if h_dif > 0:
            drop['sediment'] = max(0, drop['sediment'] - h_dif)
        else:
            c = max(-h_dif, self.min_slope) * drop['vel'] * drop['water'] * self.capacity
            if drop['sediment'] > c:
                drop['sediment'] -= (drop['sediment'] - c) * self.deposition
            else:
                available_sediment = min((c - drop['sediment']) * self.erosion, -h_dif)
                drop['sediment'] += available_sediment
                # 使用list索引方式进行赋值
                self.heightmap[int(pos[1])][int(pos[0])] -= available_sediment

        # Fix sqrt of negative value issue
        if h_dif < 0:
            # Going downhill - add energy
            drop['vel'] = math.sqrt(drop['vel']**2 + abs(h_dif) * self.gravity)
        else:
            # Going uphill - subtract energy, but ensure velocity remains positive
            new_v_squared = max(0.1, drop['vel']**2 - h_dif * self.gravity)
            drop['vel'] = math.sqrt(new_v_squared)
        
        drop['water'] *= (1 - self.evaporation)
        drop['pos'] = new_pos
        drop['dir'] = new_dir
        return drop

    def simulate(self, num_drops):
        """
        进行水力侵蚀模拟。
        :param num_drops: 模拟的粒子数量
        :return: 侵蚀后的地形高度图
        """
        for _ in range(num_drops):
            # 使用标准Python随机函数替代numpy
            pos = [random.random() * self.heightmap_width, random.random() * self.heightmap_height]
            dir_x, dir_y = random.uniform(-1, 1), random.uniform(-1, 1)
            
            # 归一化方向向量
            dir_length = math.sqrt(dir_x**2 + dir_y**2)
            if dir_length > 0:
                dir_x /= dir_length
                dir_y /= dir_length
                
            drop = {
                'pos': pos,
                'dir': [dir_x, dir_y],
                'vel': 1.0,
                'water': 1.0,
                'sediment': 0.0
            }
            
            for _ in range(self.max_path):
                drop = self.update_drop(drop)
                if drop is None:
                    break
        return self.heightmap
