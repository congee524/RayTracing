import math

from vec import Vec3, Point
from ray import Ray


class Camera():

    def __init__(self, look_from, look_at, vup, vfov, aspect):
        self.theta = vfov * math.pi / 180
        self.half_h = math.tan(self.theta / 2)
        self.half_w = aspect * self.half_h

        w = (look_from - look_at).normalize()
        u = vup.cross(w).normalize()
        v = w.cross(u)

        self.origin = look_from
        self.bl_corner = self.origin - u * self.half_w - v * self.half_h - w
        self.horizontal = u * self.half_w * 2
        self.vertical = v * self.half_h * 2

    def get_ray(self, u, v):
        direction = self.bl_corner - self.origin + u * self.horizontal + v * self.vertical
        return Ray(self.origin, direction)
