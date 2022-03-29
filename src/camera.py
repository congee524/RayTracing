# import math

# from vec import Vec3, Point
# from ray import Ray

# class Camera():

#     def __init__(self, look_from, look_at, vup, vfov, aspect):
#         self.theta = vfov * math.pi / 180
#         self.half_h = math.tan(self.theta / 2)
#         self.half_w = aspect * self.half_h

#         w = (look_from - look_at).normalize()
#         u = vup.cross(w).normalize()
#         v = w.cross(u)

#         self.origin = look_from
#         self.bl_corner = self.origin - u * self.half_w - v * self.half_h - w
#         self.horizontal = u * self.half_w * 2
#         self.vertical = v * self.half_h * 2

#     def get_ray(self, u, v):
#         direction = self.bl_corner - self.origin + u * self.horizontal + v * self.vertical
#         return Ray(self.origin, direction)

from vec import Vec3, Point
from ray import Ray


class Camera():

    def __init__(self,
                 origin=None,
                 bl_corner=None,
                 horizontal=None,
                 vertical=None):
        if origin is None:
            origin = Point()
        if bl_corner is None:
            bl_corner = Point(-2, -1, -1)
        if horizontal is None:
            horizontal = Vec3(4, 0, 0)
        if vertical is None:
            vertical = Vec3(0, 2, 0)
        assert isinstance(origin, Point)
        assert isinstance(bl_corner, Point)
        assert isinstance(horizontal, Vec3)
        assert isinstance(vertical, Vec3)

        self.origin = origin
        self.bl_corner = bl_corner
        self.horizontal = horizontal
        self.vertical = vertical

    def get_ray(self, u, v):
        direction = self.bl_corner - self.origin + u * self.horizontal + v * self.vertical
        return Ray(self.origin, direction)
