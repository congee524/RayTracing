from abc import ABC, abstractmethod
import random

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


class HitRecord():

    def __init__(self, p=None, normal=None, t=0., material=None):
        if p is None:
            p = Point()
        else:
            assert isinstance(p, Point), "p must be Point"
        if normal is None:
            normal = Vec3()
        else:
            assert isinstance(normal, Vec3), "normal must be Vec3"
        assert isinstance(t, (float, int)), "t must be scalar"

        assert (material is None) or isinstance(material, Material)

        self.p = p
        self.normal = normal
        self.t = float(t)
        self.material = material

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
