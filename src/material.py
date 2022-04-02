import math
import random
from abc import ABC, abstractmethod
from sqlite3 import SQLITE_CREATE_TABLE

from vec import Vec3, Color
from ray import Ray
from texture import ConstantTexture


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in, rec):
        pass

    def emitted(self, u, v, p):
        return Vec3(0)

    @classmethod
    def random_in_unit_sphere(cls):
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
        target = rec.p + rec.normal + Material.random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo.value(0, 0, rec.p)
        return attenuation, scattered


class Metal(Material):

    def __init__(self, albedo=None, fuzz=0.):
        if albedo is None:
            albedo = ConstantTexture(Color(0.8, 0.3, 0.3))
        self.albedo = albedo
        fuzz = float(fuzz)
        fuzz = fuzz if fuzz <= 1 else 1.
        self.fuzz = fuzz

    def scatter(self, r_in, rec):
        _ref_dir = Metal.reflect(r_in.direction.normalize(), rec.normal)
        ref_dir = _ref_dir + self.fuzz * Material.random_in_unit_sphere()

        scattered = Ray(rec.p, ref_dir)
        attenuation = self.albedo.value(0, 0, rec.p)

        if Vec3.dot(ref_dir, rec.normal) > 0:
            return attenuation, scattered
        return None, None

    @classmethod
    def reflect(cls, r_in, normal):
        return r_in - 2 * Vec3.dot(r_in, normal) * normal


class DiffuseLight(Material):

    def __init__(self, _emit):
        self.emit = _emit

    def scatter(self, r_in, rec):
        return None, None

    def emitted(self, u, v, p):
        light = self.emit.value(u, v, p)
        return light
