import random
import math
from functools import reduce

from vec import Vec3
from ray import Ray
from sampler import get_sampler
from .hittable import Hittable, HitRecord, Aabb, HittableList


class XyRect(Hittable):

    def __init__(self, x0, x1, y0, y1, k, mat):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.k = k
        self.mat = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.z) / r.direction.z
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.x < self.x0 or p.x > self.x1 or p.y < self.y0 or p.y > self.y1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.mat = self.mat
        hit_rec.t = t
        hit_rec.normal = Vec3(0, 0, 1)
        hit_rec.u = (p.x - self.x0) / (self.x1 - self.x0)
        hit_rec.v = (p.y - self.y0) / (self.y1 - self.y0)

        return hit_rec

    def bounding_box(self):
        return Aabb(Vec3(self.x0, self.y0, self.k - 0.0001),
                    Vec3(self.x1, self.y1, self.k + 0.0001))


class XzRect(Hittable):

    def __init__(self, x0, x1, z0, z1, k, mat):
        self.x0 = x0
        self.x1 = x1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.mat = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.y) / r.direction.y
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.x < self.x0 or p.x > self.x1 or p.z < self.z0 or p.z > self.z1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.mat = self.mat
        hit_rec.t = t
        hit_rec.normal = Vec3(0, 1, 0)
        hit_rec.u = (p.x - self.x0) / (self.x1 - self.x0)
        hit_rec.v = (p.z - self.z0) / (self.z1 - self.z0)

        return hit_rec

    def pdf_value(self, origin, direction):
        hit_rec = self.hit(Ray(origin, direction), 1e-3, float('inf'))
        if hit_rec is not None:
            area = (self.x1 - self.x0) * (self.z1 - self.z0)
            dist_sqrd = hit_rec.t * hit_rec.t * direction.square()
            cosine = abs(
                Vec3.dot(direction, hit_rec.normal) / direction.length())
            return dist_sqrd / (cosine * area)
        return 0.

    def random(self, origin):
        _x = self.x0 + random.random() * (self.x1 - self.x0)
        _z = self.z0 + random.random() * (self.z1 - self.z0)
        _y = self.k
        return Vec3(_x, _y, _z) - origin

    def bounding_box(self):
        return Aabb(Vec3(self.x0, self.k - 0.0001, self.z0),
                    Vec3(self.x1, self.k + 0.0001, self.z1))


class YzRect(Hittable):

    def __init__(self, y0, y1, z0, z1, k, mat):
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.mat = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.x) / r.direction.x
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.y < self.y0 or p.y > self.y1 or p.z < self.z0 or p.z > self.z1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.mat = self.mat
        hit_rec.t = t
        hit_rec.normal = Vec3(1, 0, 0)
        hit_rec.u = (p.z - self.z0) / (self.z1 - self.z0)
        hit_rec.v = (p.y - self.y0) / (self.y1 - self.y0)

        return hit_rec

    def bounding_box(self):
        return Aabb(Vec3(self.k - 0.0001, self.y0, self.z0),
                    Vec3(self.k + 0.0001, self.y1, self.z1))


class XzDisk(Hittable):

    def __init__(self, center, radius, mat, sample_type='blue_noise'):
        self.center = center
        self.radius = float(radius)
        self.mat = mat
        self.sample_type = sample_type
        self.normal = Vec3(0, 1, 0)

    def hit(self, r, t_min, t_max):
        hit_rec = None
        if not math.isclose(r.direction.y, 0):
            t = (self.center.y - r.origin.y) / r.direction.y
            if t_min <= t <= t_max:
                p = r.at(t)
                if (p - self.center).length() < self.radius:
                    hit_rec = HitRecord()
                    hit_rec.p = p
                    hit_rec.normal = self.normal
                    hit_rec.t = t
                    hit_rec.u, hit_rec.v = self.get_disk_uv(hit_rec.p)
                    hit_rec.mat = self.mat
        return hit_rec

    def get_disk_uv(self, p):
        x_min = self.center.x - self.radius
        z_min = self.center.z - self.radius
        diam = 2 * self.radius
        u, v = (p.x - x_min) / diam, (p.z - z_min) / diam
        return u, v

    def bounding_box(self):
        _x, _y, _z = self.center
        _r = self.radius
        return Aabb(Vec3(_x - _r, _y - 0.0001, _z - _r),
                    Vec3(_x + _r, _y + 0.0001, _z + _r))

    def pdf_value(self, origin, direction):
        hit_rec = self.hit(Ray(origin, direction), 1e-3, float('inf'))
        if hit_rec is not None:
            area = math.pi * self.radius * self.radius / 4
            dist_sqrd = hit_rec.t * hit_rec.t * direction.square()
            cosine = abs(
                Vec3.dot(direction, hit_rec.normal) / direction.length())
            return dist_sqrd / (cosine * area)
        return 0.

    def random(self, origin):
        if not hasattr(self, 'sampler'):
            width = height = self.radius * 2
            self.sampler = get_sampler(self.sample_type, width, height)

        while True:
            _x, _z = self.sampler.sample()
            _p = Vec3(_x - self.radius, 0, _z - self.radius)
            if _p.length() < self.radius:
                break
        return _p + self.center - origin


class Triangle(Hittable):

    def __init__(self, p1, p2, p3, mat, sample_type='uniform'):
        e1 = p2 - p1
        e2 = p3 - p1

        self.p1, self.p2, self.p3 = p1, p2, p3
        self.normal = Vec3.cross(e2, e1).normalize()
        self.mat = mat
        self.sample_type = sample_type

        # calculate area
        _a = (p2 - p1).length()
        _b = (p3 - p1).length()
        _c = (p3 - p2).length()
        _p = (_a + _b + _c) / 2
        self.area = math.sqrt(_p * (_p - _a) * (_p - _b) * (_p - _c))

    def hit(self, r, t_min, t_max):
        e1 = self.p2 - self.p1
        e2 = self.p3 - self.p1
        direct = r.direction

        pvec = Vec3.cross(direct, e2)
        det = Vec3.dot(e1, pvec)

        if math.isclose(det, 0.):
            return None

        inv_det = 1.0 / det
        tvec = r.origin - self.p1
        u = Vec3.dot(tvec, pvec) * inv_det

        if u < 0 or u > 1:
            return None

        qvec = Vec3.cross(tvec, e1)
        v = Vec3.dot(direct, qvec) * inv_det

        if v < 0 or u + v > 1:
            return None

        t = Vec3.dot(e2, qvec) * inv_det

        if t > 0.00001 and t > t_min and t < t_max:
            hit_rec = HitRecord()
            hit_rec.t = t
            hit_rec.p = r.at(t)
            hit_rec.normal = self.normal
            hit_rec.mat = self.mat
            hit_rec.u = u
            hit_rec.v = v
            return hit_rec
        return None

    def random(self, origin):
        u = random.random()
        v = random.random()
        p = math.sqrt(v) * (1 - u) * self.p1 + u * math.sqrt(v) * self.p2 + (
            1 - math.sqrt(v)) * self.p3

        return p - origin

    def pdf_value(self, origin, direction):
        hit_rec = self.hit(Ray(origin, direction), 1e-3, float('inf'))
        if hit_rec is not None:
            dist_sqrd = hit_rec.t * hit_rec.t * direction.square()
            cosine = abs(
                Vec3.dot(direction, hit_rec.normal) / direction.length())
            return dist_sqrd / (cosine * self.area)
        return 0.

    def bounding_box(self):
        p_list = [self.p1, self.p2, self.p3]
        min_x, max_x = min([p[0] for p in p_list]), max([p[0] for p in p_list])
        min_y, max_y = min([p[1] for p in p_list]), max([p[1] for p in p_list])
        min_z, max_z = min([p[2] for p in p_list]), max([p[2] for p in p_list])

        return Aabb(Vec3(min_x, min_y, min_z), Vec3(max_x, max_y, max_z))


class XzPolygon(Hittable):

    def __init__(self, xz_list, y, mat, sample_type='uniform'):
        n_points = len(xz_list)
        if n_points < 3:
            raise RuntimeError(
                f'Polygon has at least 3 points, but get {n_points} points')

        self.normal = Vec3(0, 1, 0)

        p_list = [Vec3(px, y, pz) for px, pz in xz_list]
        obj_list = []
        for idx in range(1, n_points - 1):
            obj = Triangle(p_list[0], p_list[idx], p_list[idx + 1], mat,
                           sample_type)
            obj.normal = self.normal
            obj_list.append(obj)

        self.hit_obj_list = HittableList(obj_list)
        self.area = reduce(lambda a, b: a + b, [obj.area for obj in obj_list])

    def hit(self, r, t_min, t_max):
        return self.hit_obj_list.hit(r, t_min, t_max)

    def random(self, origin):
        u = random.random() * self.area

        cnt = 0
        for obj in self.hit_obj_list:
            cnt += obj.area
            if cnt >= u:
                return obj.random(origin)

        return self.hit_obj_list[-1].random(origin)

    def pdf_value(self, origin, direction):
        hit_rec = self.hit(Ray(origin, direction), 1e-3, float('inf'))
        if hit_rec is not None:
            dist_sqrd = hit_rec.t * hit_rec.t * direction.square()
            cosine = abs(
                Vec3.dot(direction, hit_rec.normal) / direction.length())
            return dist_sqrd / (cosine * self.area)
        return 0.

    def bounding_box(self):
        return self.obj_list.bounding_box()

    @classmethod
    def generate_random_convex_polygon(cls, n_vertexs=4, tx=554, ty=554):
        # generate convex at plane
        def random_partition(a):
            b = list()
            c = list()
            for i in range(len(a)):
                if random.randrange(2):
                    b.append(a[i])
                else:
                    c.append(a[i])
            return b, c

        def get_deltas(n):
            de = [random.random() for _ in range(n)]
            de.sort()
            dep, dem = random_partition(de[1:-1])
            dem.reverse()
            des = [de[0]] + dep + [de[-1]] + dem + [de[0]]
            deltas = [des[i] - des[i - 1] for i in range(1, len(des))]
            return deltas, (de[0], de[-1])

        x, (a1, _) = get_deltas(n_vertexs)
        y, (b1, _) = get_deltas(n_vertexs)
        random.shuffle(y)
        vectors = [(x[i], y[i]) for i in range(n_vertexs)]
        vectors.sort(key=lambda v: math.atan2(v[1], v[0]))
        points = [(0, 0)]
        for v in vectors:
            points.append((points[-1][0] + v[0], points[-1][1] + v[1]))
        xmin = min([p[0] for p in points])
        ymin = min([p[1] for p in points])
        dx = a1 - xmin
        dy = b1 - ymin
        points = [(p[0] + dx, p[1] + dy) for p in points]
        vertexs = [(int(px * tx), int(py * ty)) for px, py in points[:-1]]
        return vertexs
