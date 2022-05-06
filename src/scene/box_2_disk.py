from vec import Vec3, Point, Color
from geometry import XyRect, XzDisk, YzRect, XzRect, Box
from material import Lambertian, DiffuseLight
from texture import ConstantTexture
from hittable import HittableList, FlipNormals, RotateY, Translate
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
mat_blue = Lambertian(ConstantTexture(Color(0.05, 0.05, 0.73)))
mat_light = DiffuseLight(ConstantTexture(Color(15)))

lights_list = [FlipNormals(XzDisk(Vec3(278, 554, 280), 80, mat_light))]

obj_list = [
    # wall
    FlipNormals(YzRect(0, 555, 0, 555, 555, mat_green)),
    YzRect(0, 555, 0, 555, 0, mat_red),
    FlipNormals(XzRect(0, 555, 0, 555, 555, mat_white)),
    XzRect(0, 555, 0, 555, 0, mat_white),
    FlipNormals(XyRect(0, 555, 0, 555, 555, mat_blue)),
    # box
    Translate(RotateY(Box(Point(), Point(165, 165, 165), mat_white), -18),
              Vec3(130, 0, 65)),
    Translate(RotateY(Box(Point(), Point(165, 330, 165), mat_white), 15),
              Vec3(265, 0, 295))
]

obj_list += lights_list

lights = HittableList(lights_list)
world = HittableList(obj_list)
