import math
from abc import abstractmethod

from vec import Vec3, Point
from ray import Ray
from hittable import Hittable, Aabb


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

    def pdf_value(self, origin, direction):
        return self.obj.pdf_value(origin, direction)

    def random(self, origin):
        return self.obj.random(origin)


class Translate(Hittable):

    def __init__(self, obj, offset):
        self.obj = obj
        self.offset = offset

    def hit(self, r, t_min, t_max):
        moved_r = Ray(r.origin - self.offset, r.direction, r.time)
        hit_rec = self.obj.hit(moved_r, t_min, t_max)
        if hit_rec is not None:
            hit_rec.p += self.offset
        return hit_rec

    def bounding_box(self):
        bbox = self.obj.bounding_box()
        if bbox is not None:
            bbox = Aabb(bbox._min + self.offset, bbox._max + self.offset)
        return bbox

    def pdf_value(self, origin, direction):
        return self.obj.pdf_value(origin, direction)

    def random(self, origin):
        return self.obj.random(origin)


class Rotate(Hittable):

    def __init__(self, obj, angle):
        self.obj = obj

        radians = (math.pi / 180.0) * angle
        self.sin_theta = math.sin(radians)
        self.cos_theta = math.cos(radians)

        bbox = obj.bounding_box()
        _min = Vec3(float('inf'))
        _max = Vec3(-float('inf'))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    _x = i * bbox._max.x + (1 - i) * bbox._min.x
                    _y = j * bbox._max.y + (1 - j) * bbox._min.y
                    _z = k * bbox._max.z + (1 - k) * bbox._min.z
                    tester = self._rotate(Point(_x, _y, _z))
                    for c in range(3):
                        _max[c] = tester[c] if tester[c] > _max[c] else _max[c]
                        _min[c] = tester[c] if tester[c] < _min[c] else _min[c]
        self.bbox = Aabb(_min, _max)

    @abstractmethod
    def _rotate(self, p):
        pass

    @abstractmethod
    def _rotate_t(self, p):
        pass

    def hit(self, r, t_min, t_max):
        new_orig = self._rotate_t(r.origin)
        new_dir = self._rotate_t(r.direction)
        rotated_r = Ray(new_orig, new_dir, r.time)

        hit_rec = self.obj.hit(rotated_r, t_min, t_max)
        if hit_rec is not None:
            hit_rec.p = self._rotate(hit_rec.p)
            hit_rec.normal = self._rotate(hit_rec.normal)

        return hit_rec

    def bounding_box(self):
        return self.bbox

    def pdf_value(self, origin, direction):
        return self.obj.pdf_value(origin, direction)

    def random(self, origin):
        return self.obj.random(origin)


class RotateY(Rotate):

    def _rotate(self, p):
        _x = self.cos_theta * p.x + self.sin_theta * p.z
        _y = p.y
        _z = -self.sin_theta * p.x + self.cos_theta * p.z
        return Point(_x, _y, _z)

    def _rotate_t(self, p):
        _x = self.cos_theta * p.x - self.sin_theta * p.z
        _y = p.y
        _z = self.sin_theta * p.x + self.cos_theta * p.z
        return Point(_x, _y, _z)


class RotateX(Rotate):

    def _rotate(self, p):
        _x = p.x
        _y = self.cos_theta * p.y - self.sin_theta * p.z
        _z = self.sin_theta * p.y + self.cos_theta * p.z
        return Point(_x, _y, _z)

    def _rotate_t(self, p):
        _x = p.x
        _y = self.cos_theta * p.y + self.sin_theta * p.z
        _z = -self.sin_theta * p.y + self.cos_theta * p.z
        return Point(_x, _y, _z)


class RotateZ(Rotate):

    def _rotate(self, p):
        _x = self.cos_theta * p.x - self.sin_theta * p.y
        _y = self.sin_theta * p.x + self.cos_theta * p.y
        _z = p.z
        return Point(_x, _y, _z)

    def _rotate_t(self, p):
        _x = self.cos_theta * p.x + self.sin_theta * p.y
        _y = -self.sin_theta * p.x + self.cos_theta * p.y
        _z = p.z
        return Point(_x, _y, _z)
