from vec import Vec3, Point, Color
from material import Lambertian, DiffuseLight, Metal
from texture import ConstantTexture, CheckerTexture
from object import (HittableList, XyRect, YzRect, XzRect, FlipNormals,
                    Triangle, Cylinder, Sphere)
from camera import Camera

rows = 400
columns = 300
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
mat_yellow = Metal(ConstantTexture(Color(0.9, 0.9, 0.05)), 0.3)
mat_blue = Lambertian(ConstantTexture(Color(0.12, 0.15, 0.85)))
mat_light = DiffuseLight(ConstantTexture(Color(15)))
mat_checker = Metal(
    CheckerTexture(ConstantTexture(Color(0.2, 0.3, 0.1)),
                   ConstantTexture(Color(0.9, 0.9, 0.9))), 0.3)

obj_list = [
    FlipNormals(YzRect(0, 555, 0, 555, 555, mat_green)),
    YzRect(0, 555, 0, 555, 0, mat_red),
    Cylinder(Vec3(278, 556, 280), 4, 80, mat_light),
    FlipNormals(XzRect(0, 555, 0, 555, 555, mat_white)),
    XzRect(0, 555, 0, 555, 0, mat_white),
    FlipNormals(XyRect(0, 555, 0, 555, 555, mat_white)),
    Triangle(Vec3(278, 0, 227), Vec3(213, 0, 332), Vec3(343, 0, 332),
             mat_yellow),
    FlipNormals(
        Triangle(Vec3(278, 0, 227), Vec3(213, 0, 332), Vec3(278, 150, 280),
                 mat_yellow)),
    Triangle(Vec3(278, 0, 227), Vec3(343, 0, 332), Vec3(278, 150, 280),
             mat_yellow),
    FlipNormals(
        Triangle(Vec3(213, 0, 332), Vec3(343, 0, 332), Vec3(278, 150, 280),
                 mat_yellow)),
    Cylinder(Vec3(100, 100, 100), 200, 50, mat_blue),
    Sphere(Point(370, 370, 370), 70, mat_checker)
]

world = HittableList(obj_list)
