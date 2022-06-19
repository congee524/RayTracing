from vec import Vec3, Point, Color
from material import Lambertian, DiffuseLight
from texture import ConstantTexture
from object import (HittableList, FlipNormals, XyRect, YzRect, XzRect, Box)
from camera import Camera

rows = 200
columns = 150
look_from = Point(278, 278, -800)
look_at = Point(278, 278, 0)
focus = 10
aspect = float(rows) / float(columns)
vfov = 40.
aperture = 0.
camera = Camera(look_from, look_at, Vec3(0, 1, 0), vfov, aspect, aperture,
                focus)

mat_red = Lambertian(ConstantTexture(Color(0.65, 0.05, 0.05)))
mat_white = Lambertian(ConstantTexture(Color(0.73, 0.73, 0.73)))
mat_green = Lambertian(ConstantTexture(Color(0.12, 0.45, 0.15)))
mat_light = DiffuseLight(ConstantTexture(Color(15)))

obj_list = [
    # wall
    FlipNormals(YzRect(0, 555, 0, 555, 555, mat_green)),
    YzRect(0, 555, 0, 555, 0, mat_red),
    XzRect(213, 343, 227, 332, 554, mat_light),
    FlipNormals(XzRect(0, 555, 0, 555, 555, mat_white)),
    XzRect(0, 555, 0, 555, 0, mat_white),
    FlipNormals(XyRect(0, 555, 0, 555, 555, mat_white)),
    # box
    Box(Point(130, 0, 65), Point(295, 165, 230), mat_white),
    Box(Point(265, 0, 295), Point(430, 330, 460), mat_white)
]

world = HittableList(obj_list)
