import math
import random
from abc import ABC, abstractmethod
from sqlite3 import SQLITE_CREATE_TABLE

from vec import Vec3, Color
from ray import Ray
from texture import ConstantTexture


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
            albedo = ConstantTexture(Color(0.8, 0.3, 0.3))
        self.albedo = albedo

    def scatter(self, r_in, rec):
        # r_in is useless in Lambertian scatter
        direction = rec.normal + Material.random_unit_sphere()
        if direction.near_zero():
            direction = rec.normal

        scattered = Ray(rec.p, direction)
        attenuation = self.albedo.value(0, 0, rec.p)

        return attenuation, scattered


class Metal(Material):

    def __init__(self, albedo=None, fuzz=0.):
        if albedo is None:
            albedo = ConstantTexture(Color(0.8, 0.3, 0.3))
        self.albedo = albedo
        fuzz = float(fuzz)
        fuzz = fuzz if fuzz >= 0 else 0.
        fuzz = fuzz if fuzz <= 1 else 1.
        self.fuzz = fuzz

    def scatter(self, r_in, rec):
        _ref_dir = Metal.reflect(r_in.direction().normalize(), rec.normal)
        ref_dir = _ref_dir + self.fuzz * Material.random_unit_sphere()

        scattered = Ray(rec.p, ref_dir)
        attenuation = self.albedo.value(0, 0, rec.p)

        if ref_dir * rec.normal > 0:
            return attenuation, scattered
        return None, None

    def reflect(r_in, normal):
        return r_in - normal * (2 * (r_in * normal))