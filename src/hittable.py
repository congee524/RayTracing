from abc import ABC, abstractmethod

from vec import Vec3, Point


class Hittable(ABC):

    def __init__(self, name='object'):
        assert isinstance(name, str), "name of object must be str"
        self.name = name

    @abstractmethod
    def hit(self, r, t_min, t_max, rec):
        pass


class HitRecord():

    def __init__(self, p=None, normal=None, t=0.):
        if p is None:
            p = Point()
        else:
            assert isinstance(p, Point), "p must be Point"
        if normal is None:
            normal = Vec3()
        else:
            assert isinstance(normal, Vec3), "normal must be Vec3"
        assert isinstance(t, (float, int)), "t must be scalar"

        self.p = p
        self.normal = normal
        self.t = float(t)

    def __repr__(self):
        return f"HitRecord at ({self.p}) with normal ({self.normal}) and t ({self.t})"
