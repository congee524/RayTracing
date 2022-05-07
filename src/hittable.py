import math
import random
from abc import ABC, abstractmethod

from vec import Vec3, Point
from material import Material
from aabb import Aabb
from ray import Ray


class Hittable(ABC):

    @abstractmethod
    def hit(self, r, t_min, t_max):
        pass

    @abstractmethod
    def bounding_box(self):
        pass

    def pdf_value(self, origin, direction):
        raise NotImplementedError

    def random(self, origin):
        raise NotImplementedError


class HitRecord():

    def __init__(self, p=None, normal=None, t=0., mat=None, u=0., v=0.):
        if p is None:
            p = Point()
        else:
            assert isinstance(p, Point), "p must be Point"
        if normal is None:
            normal = Vec3()
        else:
            assert isinstance(normal, Vec3), "normal must be Vec3"
        assert isinstance(t, (float, int)), "t must be scalar"

        assert (mat is None) or isinstance(mat, Material)

        self.p = p
        self.normal = normal
        self.t = float(t)
        self.mat = mat
        # position
        self.u = u
        self.v = v

    def __repr__(self):
        return f"HitRecord at ({self.p}) with normal ({self.normal}) and t ({self.t})"


class HittableList(Hittable):

    def __init__(self, *args):
        if len(args) == 0:
            self.objs = list()
        elif len(args) == 1:
            hittable_objs = args[0]
            assert isinstance(hittable_objs, (tuple, list))
            self.objs = list(hittable_objs)
        else:
            raise TypeError("HittableList accepts at most 1 params!")

    def append(self, to_append):
        assert isinstance(to_append, Hittable), "hittable_obj must be Hittable"
        if isinstance(to_append, HittableList):
            self.objs += to_append.objs
        else:
            self.objs.append(to_append)
        return self

    def bounding_box(self):
        box = None
        for obj in self.objs:
            box = Aabb.surrounding_box(box, obj.bounding_box())
        return box

    def hit(self, r, t_min, t_max):
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        hit_rec = None
        temp_t = t_max

        for hittable_obj in self.objs:
            temp_hit_rec = hittable_obj.hit(r, t_min, temp_t)
            if temp_hit_rec is not None:
                hit_rec = temp_hit_rec
                temp_t = temp_hit_rec.t

        return hit_rec


def compareX(obj):
    box = obj.bounding_box()
    assert box is not None
    return box._min[0]


def compareY(obj):
    box = obj.bounding_box()
    assert box is not None
    return box._min[1]


def compareZ(obj):
    box = obj.bounding_box()
    assert box is not None
    return box._min[2]


class BvhNode(Hittable):

    def __init__(self, world, time0, time1):
        axis = random.randint(0, 2)
        if axis == 0:
            world = sorted(world, key=compareX)
        elif axis == 1:
            world = sorted(world, key=compareY)
        else:
            world = sorted(world, key=compareZ)
        n = len(world)
        if n == 1:
            self.left = world
            self.right = world
        elif n == 2:
            self.left = world[0]
            self.right = world[1]
        else:
            self.left = BvhNode(world[:n // 2 + 1], time0, time1)
            self.right = BvhNode(world[n // 2:], time0, time1)

        box_left = self.left.bounding_box()
        box_right = self.right.bounding_box()
        self.box = Aabb.surrounding_box(box_left, box_right)

    def bounding_box(self):
        return self.box

    def hit(self, r, t_min, t_max):
        if self.box.hit(r, t_min, t_max):
            left_rec = self.left.hit(r, t_min, t_max)
            right_rec = self.right.hit(r, t_min, t_max)
            if (left_rec is not None) and (right_rec is not None):
                if left_rec.t < right_rec.t:
                    return left_rec
                else:
                    return right_rec
            elif left_rec is not None:
                return left_rec
            elif right_rec is not None:
                return right_rec

        return None


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
