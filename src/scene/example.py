from vec import Point, Color
from sphere import Sphere
from material import Lambertian, Metal
from hittable_list import HittableList

obj_list = [
    Sphere(Point(0.0, 0.0, -1.0), 0.5, Lambertian(Color(0.1, 0.2, 0.5))),
    Sphere(Point(0.0, -100.5, -1.0), 100.0, Metal(Color(0.8, 0.8, 0),
                                                  fuzz=0.3)),
    Sphere(Point(-1.0, 0.0, -1.0), 0.5, Metal(Color(0., 0., 1.), fuzz=0.)),
    Sphere(Point(1.0, 0.0, -1.0), 0.5, Lambertian(Color(1., 0., 0.)))
]

world = HittableList(obj_list)
