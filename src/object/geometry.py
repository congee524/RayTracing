import itertools
import math

from vec import Point, Vec3
from ray import Ray
from hittable import Hittable, HitRecord, HittableList, Aabb
from transform import FlipNormals
from element import XyRect, XzRect, YzRect, Triangle


class Sphere(Hittable):

    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = float(radius)
        self.mat = mat

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
        hit_rec.mat = self.mat

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
        self.mat = m

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
        hit_rec.mat = self.mat

        return hit_rec

    def bounding_box(self):
        _radius = Vec3(self.radius)
        box0 = Aabb(self.center0 - _radius, self.center0 + _radius)
        box1 = Aabb(self.center1 - _radius, self.center1 + _radius)
        return Aabb.surrounding_box(box0, box1)


class Pyramid(Hittable):

    def __init__(self, p1, p2, p3, p4, mat):
        pyramid_center = (p1 + p2 + p3 + p4) / 4
        obj_list = []
        for p_list in itertools.combinations([p1, p2, p3, p4], 3):
            surf = Triangle(*p_list, mat)
            surf_center = sum(p_list) / 3
            if Vec3.dot(surf.normal, pyramid_center - surf_center) > 0.:
                obj_list.append(surf)
            else:
                obj_list.append(FlipNormals(surf))

        self.mat = mat
        self.hit_obj_list = HittableList(obj_list)
        self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4

    def hit(self, r, t_min, t_max):
        return self.hit_obj_list.hit(r, t_min, t_max)

    def bounding_box(self):
        p_list = [self.p1, self.p2, self.p3, self.p4]
        min_x, max_x = min([p[0] for p in p_list]), max([p[0] for p in p_list])
        min_y, max_y = min([p[1] for p in p_list]), max([p[1] for p in p_list])
        min_z, max_z = min([p[2] for p in p_list]), max([p[2] for p in p_list])

        return Aabb(Vec3(min_x, min_y, min_z), Vec3(max_x, max_y, max_z))


class Cylinder(Hittable):

    def __init__(self, cen, h, r, mat):
        self.center = cen
        self.height = float(h)
        self.radius = float(r)
        self.mat = mat

    def hit(self, r, t_min, t_max):
        temp_t = t_max
        hit_rec = None

        # calculate the intersection in the two bottom surface
        if not math.isclose(r.direction.y, 0):
            surf1_center = self.center + Vec3(0, self.height / 2, 0)
            surf2_center = self.center - Vec3(0, self.height / 2, 0)
            t1 = (surf1_center.y - r.origin.y) / r.direction.y
            p1 = r.at(t1)
            if (p1 - surf1_center).length() < self.radius:
                if t_min < t1 < t_max:
                    temp_t = t1
                    hit_rec = HitRecord()
                    hit_rec.p = p1
                    hit_rec.normal = Vec3(0, 1, 0)
                    hit_rec.t = temp_t
                    hit_rec.mat = self.mat
            t2 = (surf2_center.y - r.origin.y) / r.direction.y
            p2 = r.at(t2)
            if (p2 - surf2_center).length() < self.radius:
                if t_min < t2 < temp_t:
                    temp_t = t2
                    hit_rec = HitRecord()
                    hit_rec.p = p2
                    hit_rec.normal = Vec3(0, -1, 0)
                    hit_rec.t = temp_t
                    hit_rec.mat = self.mat

        # calculate the intersection in the side
        if math.isclose(r.direction.x, 0.) and math.isclose(r.direction.z, 0.):
            return hit_rec

        _origin = Vec3(r.origin.x, 0, r.origin.z)
        _direction = Vec3(r.direction.x, 0, r.direction.z)
        _center = Vec3(self.center.x, 0, self.center.z)
        oc = _origin - _center
        a = Vec3.dot(_direction, _direction)
        half_b = Vec3.dot(oc, _direction)
        c = Vec3.dot(oc, oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0.:
            return hit_rec

        sqrtd = math.sqrt(discriminant)
        t1 = (-half_b - sqrtd) / a
        p1 = r.at(t1)
        if surf2_center.y < p1.y < surf1_center.y:
            if t_min < t1 < temp_t:
                temp_t = t1
                hit_rec = HitRecord()
                hit_rec.p = p1
                hit_rec.normal = Vec3(p1.x - self.center.x, 0,
                                      p1.z - self.center.z).normalize()
                hit_rec.t = temp_t
                hit_rec.mat = self.mat

        t2 = (-half_b + sqrtd) / a
        p2 = r.at(t2)
        if surf2_center.y < p2.y < surf1_center.y:
            if t_min < t1 < temp_t:
                temp_t = t2
                hit_rec = HitRecord()
                hit_rec.p = p2
                hit_rec.normal = Vec3(p2.x - self.center.x, 0,
                                      p2.z - self.center.z).normalize()
                hit_rec.t = temp_t
                hit_rec.mat = self.mat

        return hit_rec

    def bounding_box(self):
        _min = Vec3(self.center.x - self.radius,
                    self.center.y - self.height / 2,
                    self.center.z - self.radius)
        _max = Vec3(self.center.x + self.radius,
                    self.center.y + self.height / 2,
                    self.center.z + self.radius)
        return Aabb(_min, _max)


class Box(Hittable):

    def __init__(self, p_min, p_max, mat):
        obj_list = [
            XyRect(p_min.x, p_max.x, p_min.y, p_max.y, p_max.z, mat),
            FlipNormals(
                XyRect(p_min.x, p_max.x, p_min.y, p_max.y, p_min.z, mat)),
            XzRect(p_min.x, p_max.x, p_min.z, p_max.z, p_max.y, mat),
            FlipNormals(
                XzRect(p_min.x, p_max.x, p_min.z, p_max.z, p_min.y, mat)),
            YzRect(p_min.y, p_max.y, p_min.z, p_max.z, p_max.x, mat),
            FlipNormals(
                YzRect(p_min.y, p_max.y, p_min.z, p_max.z, p_min.x, mat))
        ]

        self.p_min = p_min
        self.p_max = p_max
        self.hit_obj_list = HittableList(obj_list)

    def hit(self, r, t_min, t_max):
        return self.hit_obj_list.hit(r, t_min, t_max)

    def bounding_box(self):
        return Aabb(self.p_min, self.p_max)
