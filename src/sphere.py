from vec import Vec3
from hittable import Hittable


class Sphere(Hittable):

    def __init__(self, center, radius, name='Sphere'):
        if not isinstance(center, Vec3):
            raise TypeError("Center point must be Point!")

        if isinstance(radius, float) or isinstance(radius, int):
            raidus = float(raidus)
        else:
            raise TypeError("Raidus must be scalar!")

        self.center = center
        self.radius = radius

    def hit(self, ray, t_min, t_max, hit_record):
        # only record the nearest intersection
        pass
