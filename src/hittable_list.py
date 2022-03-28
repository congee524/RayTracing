from numpy import isin
from vec import Point
from ray import Ray
from hittable import Hittable, HitRecord


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
                if temp_t > temp_hit_rec.t:
                    hit_anything = True
                    temp_t = temp_hit_rec.t
                    rec.t = temp_hit_rec.t
                    rec.p = temp_hit_rec.p
                    rec.normal = temp_hit_rec.normal

        return hit_anything
