from abc import ABC, abstractmethod

from vec import Vec3, Point
from material import Material
from aabb import Aabb
from ray import Ray


class Hittable(ABC):

    @abstractmethod
    def hit(self, r, t_min, t_max, rec):
        pass

    @abstractmethod
    def get_box():
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

    def hit(self, r, t_min, t_max, rec):
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(rec, HitRecord), "rec must be HitRecord"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        temp_hit_rec = HitRecord()
        temp_t = t_max
        hit_anything = False

        for hittable_obj in self.objs:
            if hittable_obj.hit(r, t_min, temp_t, temp_hit_rec):
                hit_anything = True
                temp_t = temp_hit_rec.t
                rec.t = temp_hit_rec.t
                rec.p = temp_hit_rec.p
                rec.normal = temp_hit_rec.normal
                rec.material = temp_hit_rec.material

        return hit_anything


class BvhNode(Hittable):
    pass
