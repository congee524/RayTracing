import math
import random
import itertools
import numpy as np
from collections import deque


class PoissonSampler():

    def __init__(self, width, height, min_dist=5, num_points_per_iter=16):
        self.width = width
        self.height = height
        self.min_dist = min_dist
        self.num_points_per_iter = num_points_per_iter

        self.cell_size = min_dist / math.sqrt(2)
        self.grid_w = math.ceil(self.width / self.cell_size)
        self.grid_h = math.ceil(self.height / self.cell_size)

        self.sample_points = deque()
        self.generate_poisson()

    def get_grid_pos(self, point):
        x, y = point
        return (int(x / self.cell_size), int(y / self.cell_size))

    def generate_random_point_around(self, point):
        x, y = point
        alpha = np.random.random(self.num_points_per_iter) * math.pi * 2.0
        r = (np.random.random(self.num_points_per_iter) + 1) * self.min_dist
        new_x = np.cos(alpha) * r + x
        new_y = np.sin(alpha) * r + y
        return np.dstack((new_x, new_y))[0]

    def generate_random_point(self):
        return (random.random() * self.width, random.random() * self.height)

    def draw_pic(self, points):
        import matplotlib.pyplot as plt
        plt.figure('temp')
        plt.scatter(*list(list(t) for t in zip(*points)))
        plt.savefig('output/temp.jpg')
        plt.close()

    def check_new_point_valid(self, point):
        x, y = point

        if x <= 0 or x >= self.width or y <= 0 or y >= self.height:
            return False

        grid_x, grid_y = self.get_grid_pos((x, y))
        x_l, x_r = max(0, grid_x - 2), min(grid_x + 3, self.grid_w)
        y_l, y_r = max(0, grid_y - 2), min(grid_y + 3, self.grid_h)

        for i, j in itertools.product(range(x_l, x_r), range(y_l, y_r)):
            point_idx = self.grid[(i, j)]
            if point_idx >= 0:
                nx, ny = self.sample_points[point_idx]
                dist = math.sqrt((nx - x)**2 + (ny - y)**2)
                if dist < self.min_dist:
                    return False

        return True

    def generate_poisson(self):
        assert not self.sample_points
        activate_list = deque()
        self.grid = np.ones((self.grid_w, self.grid_h), dtype=int) * -1

        first_point = self.generate_random_point()
        activate_list.append(first_point)
        self.sample_points.append(first_point)

        while activate_list:
            activate_point = activate_list.popleft()
            random_points = self.generate_random_point_around(activate_point)
            for new_point in random_points:
                if self.check_new_point_valid(new_point):
                    activate_list.append(new_point)
                    self.sample_points.append(new_point)
                    grid_pos = self.get_grid_pos(new_point)
                    self.grid[grid_pos] = len(self.sample_points) - 1

        assert self.sample_points

    def sample(self):
        if not self.sample_points:
            return None
        return self.sample_points.popleft()
