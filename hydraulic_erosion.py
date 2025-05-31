import numpy as np


class HydraulicErosion:
    def __init__(self, heightmap, inertia=0.3, capacity=8, deposition=0.2, erosion=0.7, evaporation=0.02, min_slope=0.01, gravity=10, radius=4, max_path=64):
        """
        初始化水力侵蚀模拟类。
        :param heightmap: 地形高度图，二维numpy数组
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
        self.heightmap_height, self.heightmap_width = heightmap.shape

    def interpolate_gradient(self, pos):
        """
        计算粒子当前位置的梯度。
        :param pos: 粒子位置，二维坐标 (x, y)
        :return: 梯度向量 (gx, gy)
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
        
        # 使用安全索引计算梯度，并转换为float类型避免溢出
        h00 = float(self.heightmap[x_floor, y_floor])
        h10 = float(self.heightmap[x_next, y_floor])
        h01 = float(self.heightmap[x_floor, y_next])
        h11 = float(self.heightmap[x_next, y_next])
        
        # 使用浮点数计算差值，避免溢出
        gx1 = h10 - h00
        gx2 = h11 - h01
        gy1 = h01 - h00
        gy2 = h11 - h10
        
        gx = gx1 * (1 - v) + gx2 * v
        gy = gy1 * (1 - u) + gy2 * u
        return np.array([gx, gy])

    def update_drop(self, drop):
        """
        更新粒子的状态，包括位置、速度、携带的沉积物等。
        :param drop: 粒子信息，字典包含 'pos', 'dir','vel', 'water','sediment'
        :return: 更新后的粒子信息
        """
        pos = drop['pos']
        old_dir = drop['dir']
        gradient = self.interpolate_gradient(pos)
        new_dir = old_dir * self.inertia - gradient * (1 - self.inertia)
        new_dir = new_dir / np.linalg.norm(new_dir) if np.linalg.norm(new_dir) != 0 else np.random.randn(2)
        new_pos = pos + new_dir
        if np.any(new_pos < 0) or np.any(new_pos >= [self.heightmap_width, self.heightmap_height]):
            return None
        
        # 转换为float进行计算，避免溢出
        h_new = float(self.heightmap[int(new_pos[1]), int(new_pos[0])])
        h_old = float(self.heightmap[int(pos[1]), int(pos[0])])
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
                self.heightmap[int(pos[1]), int(pos[0])] -= available_sediment

    # Fix sqrt of negative value issue
        if h_dif < 0:
            # Going downhill - add energy
            drop['vel'] = np.sqrt(drop['vel']**2 + abs(h_dif) * self.gravity)
        else:
            # Going uphill - subtract energy, but ensure velocity remains positive
            new_v_squared = max(0.1, drop['vel']**2 - h_dif * self.gravity)
            drop['vel'] = np.sqrt(new_v_squared)
        
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
            drop = {
                'pos': np.array([np.random.rand() * self.heightmap_width, np.random.rand() * self.heightmap_height]),
                'dir': np.random.randn(2),
               'vel': 1.0,
                'water': 1.0,
               'sediment': 0.0
            }
            drop['dir'] = drop['dir'] / np.linalg.norm(drop['dir'])
            for _ in range(self.max_path):
                drop = self.update_drop(drop)
                if drop is None:
                    break
        return self.heightmap
