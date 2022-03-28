import time
import argparse
import itertools
import random
import os.path as osp

import numpy as np
import cv2
from joblib import Parallel, delayed

from vec import Vec3, Point, Color
from ray import Ray
from hittable import HitRecord
from hittable_list import HittableList
from camera import Camera


def cal_color(r, world, depth):
    assert isinstance(r, Ray), "r must be Ray"
    assert isinstance(world, HittableList), 'world must be HittableList'
    assert isinstance(depth, int), 'depth must be int'
    if depth >= 50:
        return Vec3(0)

    hit_rec = HitRecord()

    if world.hit(r, 0, float('inf'), hit_rec):
        scattered = Ray(Point(), Vec3())
        attenuation = Color()
        hit_rec.material.scatter(r, hit_rec, attenuation, scattered)
        return attenuation * cal_color(scattered, world, depth + 1)

    t = 0.5 * r.direction().normalize().y + 0.5
    return (1.0 - t) * Color(1, 1, 1) + t * Color(0.5, 0.7, 1.0)


def ray_tracing(output_file):
    f_out_name = osp.join(osp.dirname(__file__), "..", output_file)

    rows = 200
    columns = 100
    samples = 100

    camera = Camera()

    import scene.example as scene
    world = scene.world

    def cal_ray_tracing(i, j):
        u = float(i + random.random()) / rows
        v = float(j + random.random()) / columns
        ray_r = camera.get_ray(u, v)
        color = cal_color(ray_r, world, 0)
        return (i, j, color)

    results = Parallel(n_jobs=-1)(
        delayed(cal_ray_tracing)(i, j)
        for i, j in itertools.product(range(rows), range(columns))
        for _ in range(samples))

    img = np.zeros((rows, columns, 3), float)
    for i, j, color in results:
        img[i][j] += color
    img /= samples
    img = (img * 255.99).astype(int)

    img = img.transpose(1, 0, 2)
    cv2.imwrite(f_out_name, img[::-1, :, ::-1])


def parse_args():
    """Parse args to get scene_file and output_file."""
    parser = argparse.ArgumentParser(description='Ray Tracing in Python')
    parser.add_argument('--output',
                        type=str,
                        default='output/output_1.jpg',
                        help='output file')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    start_time = time.time()
    ray_tracing(args.output)
    end_time = time.time()

    print(f"Total time: {end_time - start_time}")
