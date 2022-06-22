import random
from abc import ABC, abstractmethod

from vec import Vec3, Point
from material import Material
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

    def __getitem__(self, key):
        return self.objs[key]

    def __setitem__(self, key, val):
        self.objs[key] = val

    def __len__(self):
        return len(self.objs)

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


def fmin(a, b):
    return a if a < b else b


def fmax(a, b):
    return a if a > b else b


class Aabb():

    def __init__(self, a, b):
        self._min = a
        self._max = b

    def hit(self, r, t_min, t_max):
        for i in range(3):
            div = 1.0 / r.direction[i]
            t1 = (self._min[i] - r.origin[i]) * div
            t2 = (self._max[i] - r.origin[i]) * div
            if div < 0.:
                t1, t2 = t2, t1
            t_min = t1 if t1 > t_min else t_min
            t_max = t2 if t2 < t_max else t_max
            if t_max <= t_min:
                return False

        return True

    def surrounding_box(box0, box1):
        if box0 is None:
            return box1
        if box1 is None:
            return box0
        small = Vec3([fmin(box0._min[i], box1._min[i]) for i in range(3)])
        big = Vec3([fmax(box0._max[i], box1._max[i]) for i in range(3)])
        return Aabb(small, big)


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
