import math
import random
from abc import ABC, abstractmethod
from pdf import CosinePDF

from vec import Vec3, Color
from ray import Ray
from texture import ConstantTexture


class ScatterRecord():

    def __init__(self, atten=None, sct_ray=None, pdf=None, is_specular=False):
        self.atten = atten
        self.sct_ray = sct_ray
        self.pdf = pdf
        self.is_specular = is_specular


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in, rec):
        pass

    def emitted(self, r_in, rec):
        raise NotImplementedError

    def scatter_pdf(self, r_in, rec, scattered):
        raise NotImplementedError

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
            albedo = ConstantTexture(
                Color(random.random(), random.random(), random.random()))
        self.albedo = albedo

    def scatter(self, r_in, rec):
        atten = self.albedo.value(rec.u, rec.v, rec.p)
        pdf = CosinePDF(rec.normal)
        sct_rec = ScatterRecord(atten=atten, pdf=pdf)
        return sct_rec

    def scatter_pdf(self, r_in, rec, scattered):
        cos = Vec3.dot(rec.normal, scattered.direction.normalize())
        cos = cos if cos > 0. else 0.
        return cos / math.pi

    def emitted(self, r_in, rec):
        return Vec3(0)


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
        sct_ray = Ray(rec.p, ref_dir)
        atten = self.albedo.value(rec.u, rec.v, rec.p)

        if Vec3.dot(ref_dir, rec.normal) > 0:
            return ScatterRecord(atten=atten,
                                 sct_ray=sct_ray,
                                 is_specular=True)
        return ScatterRecord()

    def emitted(self, r_in, rec):
        return Vec3(0)

    @classmethod
    def reflect(cls, r_in, normal):
        return r_in - 2 * Vec3.dot(r_in, normal) * normal


class DiffuseLight(Material):

    def __init__(self, _emit):
        self.emit = _emit

    def scatter(self, r_in, rec):
        return ScatterRecord()

    def emitted(self, r_in, rec):
        if Vec3.dot(rec.normal, r_in.direction) < 0.:
            return self.emit.value(rec.u, rec.v, rec.p)
        return Vec3(0)


class Microfacet(Material):

    def __init__(self, roughness=0.6, index_of_reflect=0.1, albedo=None):
        assert 0 <= roughness <= 1, (
            f'roughness must be in [0, 1], but get {roughness}')
        assert 0 < index_of_reflect < 1, (
            f'ior must be in (0, 1), but get {index_of_reflect}')
        if albedo is None:
            albedo = ConstantTexture(
                Color(random.random(), random.random(), random.random()))

        self.rough = roughness
        self.albedo = albedo
        self.ior = index_of_reflect

        # temp vars for F G D function
        f0 = (1 - self.ior) / (1 + self.ior)
        self.f0 = f0 * f0
        self.alpha2 = self.rough * self.rough

    def emitted(self, r_in, rec):
        return Vec3(0)

    def scatter(self, r_in, rec):
        atten = self.albedo.value(rec.u, rec.v, rec.p)

        if math.isclose(self.rough, 0.):
            ref_dir = Metal.reflect(r_in.direction.normalize(), rec.normal)
            sct_ray = Ray(rec.p, ref_dir)
            atten = self.albedo.value(rec.u, rec.v, rec.p)
            cosine = Vec3.dot(ref_dir, rec.normal)
            if cosine > 0:
                atten *= self.fresnel_schlick(cosine)
                sct_rec = ScatterRecord(atten=atten,
                                        sct_ray=sct_ray,
                                        is_specular=True)
            else:
                sct_rec = ScatterRecord()
        else:
            pdf = CosinePDF(rec.normal)
            sct_rec = ScatterRecord(atten=atten, pdf=pdf)

        return sct_rec

    def scatter_pdf(self, r_in, rec, scattered):
        wv = -r_in.direction.normalize()
        wl = scattered.direction.normalize()
        n = rec.normal.normalize()
        m = (wv + wl).normalize()

        ldotn = Vec3.dot(wl, n)
        ldotm = Vec3.dot(wl, m)
        vdotn = Vec3.dot(wv, n)
        vdotm = Vec3.dot(wv, m)
        mdotn = Vec3.dot(m, n)

        if ldotn <= 0:
            return 0.

        F = self.fresnel_schlick(vdotm)
        G = self.geom_GGX(ldotn, ldotm, vdotn, vdotm)
        D = self.norm_dist_GGX(mdotn)

        # f(l, v) * cosine = F * G * D * ldotn / (4 * vdotn * ldotn)
        return F * G * D / (4 * vdotn)

    def fresnel_schlick(self, cosine):
        return self.f0 + (1 - self.f0) * math.pow(1 - cosine, 5)

    def geom_GGX(self, ldotn, ldotm, vdotn, vdotm):

        def partial_geom_GGX(wdotm, wdotn):
            if wdotm / wdotn <= 0:
                return 0.
            wdotm2 = wdotm * wdotm
            tan2 = (1 - wdotm2) / wdotm2
            return 2. / (1 + math.sqrt(1 + self.alpha2 * tan2))

        return partial_geom_GGX(ldotn, ldotm) * partial_geom_GGX(vdotn, vdotm)

    def norm_dist_GGX(self, mdotn):
        if mdotn <= 0:
            return 0.
        mdotn2 = mdotn * mdotn
        den = mdotn2 * self.alpha2 + (1 - mdotn2)
        return self.alpha2 / (math.pi * den * den)
