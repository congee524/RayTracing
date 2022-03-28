import math
import random
from abc import ABC, abstractmethod

from vec import Vec3, Color


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass


def random_unit_sphere():
    r = random.random()
    phi = math.pi * random.random()
    theta = 2 * math.pi * random.random()

    p = Vec3(r * math.cos(theta) * math.sin(phi),
             r * math.sin(theta) * math.sin(phi), r * math.cos(phi))
    return p


class Lambertian(Material):

    def __init__(self, albedo=None):
        if albedo is None:
            albedo = Color(0.8, 0.3, 0.3)
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        # r_in is useless in Lambertian scatter

        direction = rec.normal + random_unit_sphere()
        if direction.near_zero():
            direction = rec.normal

        scattered.orig = rec.p
        scattered.dir = direction

        for i in range(3):
            attenuation[i] = self.albedo[i]

        return True