from vec import Point, Color
from sphere import Sphere
from material import Lambertian
from hittable_list import HittableList

obj_list = [
    Sphere(Point(0.0, 0.0, -1.0), 0.5, Lambertian(Color(0.8, 0.3, 0.3))),
    Sphere(Point(0.0, -100.5, -1.0), 100.0, Lambertian(Color(0.8, 0.8, 0))),
    Sphere(Point(1.0, 0.0, -1.0), 0.5, Lambertian(Color(0.8, 0.6, 0.2))),
    Sphere(Point(-1.0, 0.0, -1.0), 0.5, Lambertian(Color(0.8, 0.8, 0.8)))
]

world = HittableList(obj_list)
