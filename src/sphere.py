import math

from vec import Point, Vec3
from ray import Ray
from hittable import Hittable, HitRecord
from material import Material
from aabb import Aabb


class Sphere(Hittable):

    def __init__(self, center, radius, material):
        assert isinstance(center, Point), "Center point must be Point"
        assert isinstance(radius, (float, int)), "Raidus must be scalar"
        assert isinstance(material, Material), 'material must be Material'

        self.center = center
        self.radius = float(radius)
        self.material = material

    def hit(self, r, t_min, t_max):
        # only record the nearest intersection
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        oc = r.origin() - self.center
        a = r.direction() * r.direction()
        half_b = oc * r.direction()
        c = oc * oc - self.radius * self.radius
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
        hit_rec.material = self.material

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
        self.material = m

    def center(self, time):
        return self.center0 + (
            (time - self.time0) /
            (self.time1 - self.time0)) * (self.center1 - self.center0)

    def hit(self, r, t_min, t_max, rec):
        # only record the nearest intersection
        assert isinstance(r, Ray), "r must be Ray"
        assert isinstance(rec, HitRecord), "rec must be HitRecord"
        assert isinstance(t_min, (float, int)), "t_min must be scalar"
        assert isinstance(t_max, (float, int)), "t_max must be scalar"

        oc = r.origin() - self.center(r.time())
        a = r.direction() * r.direction()
        half_b = oc * r.direction()
        c = oc * oc - self.radius * self.radius
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
        hit_rec.normal = (hit_rec.p - self.center(r.time())) / self.radius
        hit_rec.material = self.material

        return hit_rec

    def bounding_box(self):
        _radius = Vec3(self.radius)
        box0 = Aabb(self.center0 - _radius, self.center0 + _radius)
        box1 = Aabb(self.center1 - _radius, self.center1 + _radius)
        return Aabb.surrounding_box(box0, box1)
