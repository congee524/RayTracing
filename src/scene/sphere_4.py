from vec import Vec3, Point, Color
from material import Lambertian, Metal
from texture import ConstantTexture, CheckerTexture
from object import HittableList, Sphere
from camera import Camera

rows = 200
columns = 100
look_from = Point(3, 3, 2)
look_at = Point(0, 0, -1)
focus = (look_from - look_at).length()
aspect = float(rows) / float(columns)
camera = Camera(look_from, look_at, Vec3(0, 1, 0), 20, aspect, 2.0, focus)

mat_1 = Lambertian(ConstantTexture(Color(0.1, 0.2, 0.5)))
mat_2 = Metal(
    CheckerTexture(ConstantTexture(Color(0.2, 0.3, 0.1)),
                   ConstantTexture(Color(0.9, 0.9, 0.9))), 0.3)
mat_3 = Lambertian(ConstantTexture(Color(0., 0., 1.)))
mat_4 = Lambertian(ConstantTexture(Color(1, 0, 0)))

obj_list = [
    Sphere(Point(0, 0, -1), 0.5, mat_1),
    Sphere(Point(0, -100.5, -1), 100, mat_2),
    Sphere(Point(-1, 0, -1), 0.5, mat_3),
    Sphere(Point(1, 0, -1), 0.5, mat_4)
]

world = HittableList(obj_list)
