from vec import Vec3, Point, Color
from geometry import Pyramid, XyRect, YzRect, XzRect, Box
from material import Lambertian, DiffuseLight
from texture import ConstantTexture
from hittable import HittableList, FlipNormals, RotateX, RotateY, RotateZ, Translate
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

obj_list = [
    # wall
    FlipNormals(YzRect(0, 555, 0, 555, 555, mat_green)),
    YzRect(0, 555, 0, 555, 0, mat_red),
    XzRect(213, 343, 227, 332, 554, mat_light),
    FlipNormals(XzRect(0, 555, 0, 555, 555, mat_white)),
    XzRect(0, 555, 0, 555, 0, mat_white),
    FlipNormals(XyRect(0, 555, 0, 555, 555, mat_blue)),
    # box
    Translate(
        RotateX(RotateY(Box(Point(), Point(165, 165, 165), mat_white), -45),
                -30), Vec3(130, 200, 65)),
    Translate(
        RotateZ(RotateY(Box(Point(), Point(165, 330, 165), mat_white), 30),
                20), Vec3(265, 60, 295)),
    # pyramid
    Translate(
        RotateZ(
            RotateY(
                Pyramid(Vec3(278, 0, 227), Vec3(213, 0,
                                                332), Vec3(343, 0, 332),
                        Vec3(278, 150, 280), mat_blue), 30), 20),
        Vec3(0, 310, 0))
]

world = HittableList(obj_list)
