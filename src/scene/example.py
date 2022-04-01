from vec import Point, Color
from sphere import Sphere
from material import Lambertian, Metal
from texture import ConstantTexture, CheckerTexture
from hittable import HittableList

mat_1 = Lambertian(ConstantTexture(Color(0.1, 0.2, 0.5)))
mat_2 = Metal(CheckerTexture(ConstantTexture(Color(0.2, 0.3, 0.1)), ConstantTexture(Color(0.9, 0.9, 0.9))), 0.3)
mat_3 = Lambertian(ConstantTexture(Color(0., 0., 1.)))
mat_4 = Lambertian(ConstantTexture(Color(1, 0, 0)))

obj_list = [
    Sphere(Point(0, 0, -1), 0.5, mat_1),
    Sphere(Point(0, -100.5, -1), 100, mat_2),
    Sphere(Point(-1, 0, -1), 0.5, mat_3),
    Sphere(Point(1, 0, -1), 0.5, mat_4)
]

world = HittableList(obj_list)
