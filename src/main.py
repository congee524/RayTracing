import time
import argparse
import itertools
import random
import os.path as osp
import multiprocessing as mp

import numpy as np
# from joblib import Parallel, delayed

from vec import Vec3, Point, Color
from ray import Ray
from hittable import HittableList
from camera import Camera


def write_ppm_file(output_file, img, rows, columns):
    f_out_name = osp.join(osp.dirname(__file__), "..", output_file)
    with open(f_out_name, 'w') as f:
        title = f'P3\n{rows} {columns}\n255\n'
        f.write(title)
        for j in reversed(range(columns)):
            for i in range(rows):
                ir, ig, ib = img[j][i]
                f.write(f'{ir} {ig} {ib}\n')


def cal_color(r, world, depth):
    hit_rec = world.hit(r, 0.001, float('inf'))
    if hit_rec is not None:
        light = hit_rec.mat.emitted(hit_rec.u, hit_rec.v, hit_rec.p)
        attenuation, scattered = hit_rec.mat.scatter(r, hit_rec)
        if attenuation is not None and depth < 50:
            return light + attenuation * cal_color(scattered, world, depth + 1)
        else:
            return light

    return Color(0)


def cal_ray_tracing(i, j, samples, rows, columns, camera, world):
    color = Color(0)
    for _ in range(samples):
        u = float(i + random.random()) / rows
        v = float(j + random.random()) / columns
        ray_r = camera.get_ray(u, v)
        color += cal_color(ray_r, world, 0)
    return (i, j, color)


def ray_tracing(output_file):
    samples = 100
    use_multiprocessing = True

    # import scene.example as scene
    import scene.box_2_rotate_xyz as scene
    rows = scene.rows
    columns = scene.columns
    camera = scene.camera
    world = scene.world

    params = (samples, rows, columns, camera, world)

    if use_multiprocessing:
        n_jobs = 4
        with mp.Pool(n_jobs) as p:
            results = p.starmap(cal_ray_tracing, [(i, j) + params
                                                  for i in range(rows)
                                                  for j in range(columns)])
    else:
        results = []
        for i, j in itertools.product(range(rows), range(columns)):
            results.append(cal_ray_tracing(i, j))

    img = np.zeros((rows, columns, 3), float)
    for i, j, color in results:
        img[i][j] += color
    img /= samples
    img = (np.sqrt(img) * 255.99).astype(int)

    img = img.transpose(1, 0, 2)

    write_ppm_file(output_file, img, rows, columns)


def parse_args():
    """Parse args to get scene_file and output_file."""
    parser = argparse.ArgumentParser(description='Ray Tracing in Python')
    parser.add_argument('--output',
                        type=str,
                        default='output/output_2_3.ppm',
                        help='output file')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    start_time = time.time()
    ray_tracing(args.output)
    end_time = time.time()

    print(f"Total time: {end_time - start_time}")
