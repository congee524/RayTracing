import math
import random
from abc import abstractmethod

from onb import ONB
from vec import Vec3


class PDF():

    def value(self, direction):
        return Vec3(0)

    @abstractmethod
    def generate(self):
        raise NotImplementedError


class CosinePDF(PDF):

    def __init__(self, _w):
        self.uvw = ONB(_w)

    def value(self, direction):
        cos = Vec3.dot(direction.normalize(), self.uvw.w())
        cos = cos if cos > 0. else 0.
        return cos / math.pi

    def generate(self):
        return self.uvw.local(CosinePDF.random_cosine_direction())

    @classmethod
    def random_cosine_direction(cls):
        r = random.random()
        phi = 2 * math.pi * random.random()

        x = 2 * math.cos(phi) * math.sqrt(r)
        y = 2 * math.sin(phi) * math.sqrt(r)
        z = math.sqrt(1 - r)

        return Vec3(x, y, z)


class HitPDF(PDF):

    def __init__(self, obj, origin):
        self.obj = obj
        self.origin = origin

    def value(self, direction):
        return self.obj.pdf_value(self.origin, direction)

    def generate(self):
        return self.obj.random(self.origin)


class MixPDF(PDF):

    def __init__(self, *args):
        self.pdf_list = []
        for arg in args:
            self.pdf_list.append(arg)

        self.num_pdf = len(self.pdf_list)
        assert self.num_pdf > 0
        self.avg_pr = 1.0 / self.num_pdf

    def value(self, direction):
        return sum(
            [self.avg_pr * pdf.value(direction) for pdf in self.pdf_list])

    def generate(self):
        _rand = random.random()
        for i in range(self.num_pdf):
            if _rand < (i + 1) * self.avg_pr:
                return self.pdf_list[i].generate()
        return self.pdf_list[-1].generate()
