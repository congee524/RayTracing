import time
import os.path as osp
import argparse
import itertools

import numpy as np
import cv2

from vec import Vec3, Point, Color
from ray import Ray
from sphere import Sphere


def cal_color(r, obj_list):
    assert isinstance(r, Ray), "r must be Ray"
    # TODO: just put a shpere at (0, 0, -1) with radius 0.5 now
    sphere = obj_list[0]

    if sphere.hit(r, 0, 2):
        return Color(1, 0, 0)

    t = 0.5 * r.direction().normalize().y + 0.5

    return (1.0 - t) * Color(1, 1, 1) + t * Color(0.5, 0.7, 1.0)


def ray_tracing(scene_file, output_file):
    f_out_name = osp.join(osp.dirname(__file__), "..", output_file)

    rows = 200
    columns = 100
    img = np.zeros((columns, rows, 3), float)

    lower_left_corner = Vec3(-2, -1, -1)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Point(0.0, 0.0, 0.0)

    obj_list = []
    obj_list.append(Sphere(Point(0, 0, -1), 0.5))

    for j, i in itertools.product(reversed(range(columns)), range(rows)):
        u = float(i) / rows
        v = float(j) / columns
        ray_r = Ray(origin, lower_left_corner + horizontal * u + vertical * v)
        color = cal_color(ray_r, obj_list)
        img[j][i] = color

    img = (img * 255.99).astype(int)
    cv2.imwrite(f_out_name, img[::-1, :, ::-1])


def parse_args():
    """Parse args to get scene_file and output_file."""
    parser = argparse.ArgumentParser(description='Ray Tracing in Python')
    parser.add_argument('--scene',
                        type=str,
                        default='scene/sphere_1.txt',
                        help='scene file')
    parser.add_argument('--output',
                        type=str,
                        default='output/output_1.jpg',
                        help='output file')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    start_time = time.time()
    ray_tracing(args.scene, args.output)
    end_time = time.time()

    print(f"Total time: {end_time - start_time}")
