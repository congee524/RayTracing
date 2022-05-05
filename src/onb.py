import math
import random

from vec import Vec3


class ONB():

    def __init__(self, *args):
        self.axis = [Vec3(), Vec3(), Vec3()]

        if len(args) > 0:
            self.build_from_w(*args)

    def build_from_w(self, _w):
        self.axis[2] = _w.normalize()
        if abs(self.w().x) > 0.9:
            a = Vec3(0, 1, 0)
        else:
            a = Vec3(1, 0, 0)
        self.axis[1] = Vec3.cross(self.w(), a).normalize()
        self.axis[0] = Vec3.cross(self.w(), self.v())

    def __getitem__(self, key):
        assert isinstance(key, int), "index must be integer"
        if key == 0:
            return self.axis[0]
        elif key == 1:
            return self.axis[1]
        elif key == 2:
            return self.axis[2]
        else:
            raise IndexError("index out of range")

    def u(self):
        return self.axis[0]

    def v(self):
        return self.axis[1]

    def w(self):
        return self.axis[2]

    def local(self, *args):
        tmp = Vec3(*args)
        return tmp.x * self.u() + tmp.y * self.v() + tmp.z * self.w()

    @classmethod
    def random_direction(cls):
        r = random.random()
        phi = 2 * math.pi * random.random()

        x = 2 * math.cos(phi) * math.sqrt(r * (1 - r))
        y = 2 * math.sin(phi) * math.sqrt(r * (1 - r))
        z = 1 - 2 * r

        return Vec3(x, y, z)

    @classmethod
    def random_cosine_direction(cls):
        r = random.random()
        phi = 2 * math.pi * random.random()

        x = 2 * math.cos(phi) * math.sqrt(r)
        y = 2 * math.sin(phi) * math.sqrt(r)
        z = math.sqrt(1 - r)

        return Vec3(x, y, z)
