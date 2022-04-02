import math
import random

from vec import Vec3, Point
from ray import Ray


class Camera():

    def __init__(self,
                 look_from,
                 look_at,
                 vup,
                 vfov,
                 aspect,
                 aperture,
                 focus,
                 t0=0.,
                 t1=0.):
        """Camera

        Args:
            look_from (Point): the position of camera
            look_at (Point): the center of the screen
            vup (_type_): _description_
            vfov (int|float): vertical field of view
            aspect (_type_): _description_
        """
        self.time0 = float(t0)
        self.time1 = float(t1)
        self.lens_raidus = aperture / 2
        self.theta = vfov * math.pi / 180
        self.half_height = math.tan(self.theta / 2) * focus
        self.half_width = aspect * self.half_height

        self.w = (look_from - look_at).normalize()
        self.u = Vec3.cross(vup, self.w).normalize()
        self.v = Vec3.cross(self.w, self.u)

        self.origin = look_from
        self.bl_corner = self.origin - self.u * self.half_width - self.v * self.half_height - self.w * focus
        self.horizontal = 2 * self.u * self.half_width
        self.vertical = 2 * self.v * self.half_height

    def random_in_unit_disk():
        while True:
            p = 2 * Vec3(random.random(), random.random(), 0) - Vec3(1, 1, 0)
            if Vec3.dot(p, p) < 1:
                return p

    def get_ray(self, s, t):
        rd = self.lens_raidus * Camera.random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y
        direction = self.bl_corner + s * self.horizontal + t * self.vertical - self.origin - offset
        time = self.time0 + random.random() * (self.time1 - self.time0)
        return Ray(Point(self.origin + offset), direction, time)
