import math

from vec import Point, Vec3
from ray import Ray
from hittable import Hittable, HitRecord
from material import Material
from aabb import Aabb


class Sphere(Hittable):

    def __init__(self, center, radius, material):
        assert isinstance(center, Point), "Center point must be Point"
        assert isinstance(radius, (float, int)), "Raidus must be scalar"
        assert isinstance(material, Material), 'material must be Material'

        self.center = center
        self.radius = float(radius)
        self.material = material

    def get_sphere_uv(p):
        phi = math.atan2(p.z, p.x)
        theta = math.asin(p.y)
        u = 1 - (phi + math.pi) / (2 * math.pi)
        v = (theta + math.pi / 2) / math.pi
        return u, v

    def hit(self, r, t_min, t_max):
        # only record the nearest intersection
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        oc = r.origin - self.center
        a = Vec3.dot(r.direction, r.direction)
        half_b = Vec3.dot(oc, r.direction)
        c = Vec3.dot(oc, oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return None

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root <= t_min or root >= t_max:
            root = (-half_b + sqrtd) / a
            if root <= t_min or root >= t_max:
                return None

        hit_rec = HitRecord()
        hit_rec.p = Point(r.at(root))
        hit_rec.t = root
        hit_rec.normal = (hit_rec.p - self.center) / self.radius
        hit_rec.u, hit_rec.v = Sphere.get_sphere_uv(hit_rec.normal)
        hit_rec.material = self.material

        return hit_rec

    def bounding_box(self):
        return Aabb(self.center - Vec3(self.radius),
                    self.center + Vec3(self.radius))


class MovingSphere(Hittable):

    def __init__(self, c1, c2, t0, t1, r, m):
        self.center0 = c1
        self.center1 = c2
        self.time0 = t0
        self.time1 = t1
        self.radius = r
        self.material = m

    def center(self, time):
        return self.center0 + (
            (time - self.time0) /
            (self.time1 - self.time0)) * (self.center1 - self.center0)

    def hit(self, r, t_min, t_max):
        # only record the nearest intersection
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        oc = r.origin - self.center(r.time)
        a = Vec3.dot(r.direction, r.direction)
        half_b = Vec3.dot(oc, r.direction)
        c = Vec3.dot(oc, oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return None

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root <= t_min or root >= t_max:
            root = (-half_b + sqrtd) / a
            if root <= t_min or root >= t_max:
                return None

        hit_rec = HitRecord()
        hit_rec.p = Point(r.at(root))
        hit_rec.t = root
        hit_rec.normal = (hit_rec.p - self.center(r.time)) / self.radius
        hit_rec.u, hit_rec.v = Sphere.get_sphere_uv(hit_rec.normal)
        hit_rec.material = self.material

        return hit_rec

    def bounding_box(self):
        _radius = Vec3(self.radius)
        box0 = Aabb(self.center0 - _radius, self.center0 + _radius)
        box1 = Aabb(self.center1 - _radius, self.center1 + _radius)
        return Aabb.surrounding_box(box0, box1)


class FlipNormals(Hittable):

    def __init__(self, obj):
        self.obj = obj

    def hit(self, r, t_min, t_max):
        hit_rec = self.obj.hit(r, t_min, t_max)
        if hit_rec is not None:
            hit_rec.normal = -1 * hit_rec.normal
        return hit_rec

    def bounding_box(self):
        return self.obj.bounding_box()


class XyRect(Hittable):

    def __init__(self, x0, x1, y0, y1, k, mat):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.k = k
        self.material = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.z) / r.direction.z
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.x < self.x0 or p.x > self.x1 or p.y < self.y0 or p.y > self.y1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.material = self.material
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
        self.material = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.y) / r.direction.y
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.x < self.x0 or p.x > self.x1 or p.z < self.z0 or p.z > self.z1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.material = self.material
        hit_rec.t = t
        hit_rec.normal = Vec3(0, 1, 0)
        hit_rec.u = (p.x - self.x0) / (self.x1 - self.x0)
        hit_rec.v = (p.z - self.z0) / (self.z1 - self.z0)

        return hit_rec

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
        self.material = mat

    def hit(self, r, t_min, t_max):
        t = (self.k - r.origin.x) / r.direction.x
        if t < t_min or t > t_max:
            return None

        p = r.at(t)

        if p.y < self.y0 or p.y > self.y1 or p.z < self.z0 or p.z > self.z1:
            return None

        hit_rec = HitRecord()
        hit_rec.p = p
        hit_rec.material = self.material
        hit_rec.t = t
        hit_rec.normal = Vec3(1, 0, 0)
        hit_rec.u = (p.z - self.z0) / (self.z1 - self.z0)
        hit_rec.v = (p.y - self.y0) / (self.y1 - self.y0)

        return hit_rec

    def bounding_box(self):
        return Aabb(Vec3(self.k - 0.0001, self.y0, self.z0),
                    Vec3(self.k + 0.0001, self.y1, self.z1))
