import math
from abc import ABC, abstractmethod
from typing import Text

from vec import Vec3, Color


class Texture(ABC):

    @abstractmethod
    def value(self, u, v, p):
        pass


class ConstantTexture(Texture):

    def __init__(self, *args):
        if len(args) == 0:
            self.color = Color(0)
        elif len(args) == 1:
            self.color = args[0]
        elif len(args) == 3:
            self.color = Color(args)
        else:
            assert False, "wrong num of args"

    def value(self, u, v, p):
        return self.color


class CheckerTexture(Texture):

    def __init__(self, t0, t1):
        self.even = t0
        self.odd = t1

    def value(self, u, v, p):
        sines = math.sin(10 * p.x) * math.sin(10 * p.y) * math.sin(10 * p.z)
        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)
