import math

from vec import Point
from ray import Ray
from hittable import Hittable, HitRecord
from material import Material


class Sphere(Hittable):

    def __init__(self, center, radius, material):
        assert isinstance(center, Point), "Center point must be Point"
        assert isinstance(radius, (float, int)), "Raidus must be scalar"
        assert isinstance(material, Material), 'material must be Material'

        self.center = center
        self.radius = float(radius)
        self.material = material

    def hit(self, r, t_min, t_max, rec):
        # only record the nearest intersection
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(rec, HitRecord), "rec must be HitRecord"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        oc = r.origin() - self.center
        a = r.direction() * r.direction()
        half_b = oc * r.direction()
        c = oc * oc - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root <= t_min or root >= t_max:
            root = (-half_b + sqrtd) / a
            if root <= t_min or root >= t_max:
                return False

        rec.t = root
        rec.p = Point(r.at(rec.t))
        rec.normal = (rec.p - self.center) / self.radius
        rec.material = self.material

        return True
