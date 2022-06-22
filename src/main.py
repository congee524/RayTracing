import time
import argparse
import itertools
import random
import os.path as osp
import multiprocessing as mp

import numpy as np
from pdf import HitPDF, MixPDF

from vec import Color
from ray import Ray


def write_ppm_file(output_file, img, rows, columns):
    f_out_name = osp.join(osp.dirname(__file__), "..", output_file)
    with open(f_out_name, 'w') as f:
        title = f'P3\n{rows} {columns}\n255\n'
        f.write(title)
        for j in reversed(range(columns)):
            for i in range(rows):
                ir, ig, ib = img[j][i]
                f.write(f'{ir} {ig} {ib}\n')


def cal_ray_color(r, world, lights, depth):
    hit_rec = world.hit(r, 0.001, float('inf'))
    if hit_rec is not None:
        emitted = hit_rec.mat.emitted(r, hit_rec)
        sct_rec = hit_rec.mat.scatter(r, hit_rec)

        if sct_rec.atten is not None and depth < 50:
            if sct_rec.is_specular:
                return emitted + sct_rec.atten * cal_ray_color(
                    sct_rec.sct_ray, world, lights, depth + 1)
            else:
                hit_pdfs = [HitPDF(light, hit_rec.p) for light in lights.objs]
                pdf_list = hit_pdfs + [sct_rec.pdf]
                mix_pdf = MixPDF(pdf_list)

                sct_ray = Ray(hit_rec.p, mix_pdf.generate(), r.time)
                sct_pdf = hit_rec.mat.scatter_pdf(r, hit_rec, sct_ray)
                pdf_value = mix_pdf.value(sct_ray.direction)

                return emitted + sct_rec.atten * sct_pdf * cal_ray_color(
                    sct_ray, world, lights, depth + 1) / pdf_value

        else:
            return emitted

    return Color(0)


def cal_ray_tracing(i, j, samples, rows, columns, camera, world, lights):
    color = Color(0)
    for _ in range(samples):
        u = float(i + random.random()) / (rows - 1)
        v = float(j + random.random()) / (columns - 1)
        ray_r = camera.get_ray(u, v)
        color += cal_ray_color(ray_r, world, lights, 0)
    return (i, j, color)


def ray_tracing(args):
    output_fname = args.output
    samples = args.samples
    use_multiprocessing = True

    import scene.hw3 as scene
    rows = scene.rows
    columns = scene.columns
    camera = scene.camera
    lights = scene.lights
    world = scene.world

    params = (samples, rows, columns, camera, world, lights)

    if use_multiprocessing:
        n_jobs = 32
        with mp.Pool(n_jobs) as p:
            results = p.starmap(cal_ray_tracing, [(i, j) + params
                                                  for i in range(rows)
                                                  for j in range(columns)])
    else:
        results = []
        for i, j in itertools.product(range(rows), range(columns)):
            results.append(cal_ray_tracing(i, j, *params))

    img = np.zeros((rows, columns, 3), float)
    for i, j, color in results:
        img[i][j] += color
    img /= samples
    img = (np.sqrt(img) * 255.99).astype(int)

    img = img.transpose(1, 0, 2)

    write_ppm_file(output_fname, img, rows, columns)


def parse_args():
    """Parse args to get scene_file and output_file."""
    parser = argparse.ArgumentParser(description='Ray Tracing in Python')
    parser.add_argument('--output',
                        type=str,
                        default='output/output_3_ns_10.ppm',
                        help='output file')
    parser.add_argument('--samples',
                        type=int,
                        default=1,
                        help='num of sample lights')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    start_time = time.time()
    ray_tracing(args)
    total_time = time.time() - start_time

    with open(args.output + '.txt', 'w+') as f:
        f.writelines([f'Total time: {total_time}\n'])
    print(f'Total time: {total_time}')
