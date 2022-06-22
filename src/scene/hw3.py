from vec import Vec3, Point, Color
from material import Lambertian, DiffuseLight, Microfacet
from texture import ConstantTexture
from object import (HittableList, FlipNormals, RotateX, RotateY, RotateZ,
                    Translate, XyRect, XzDisk, YzRect, XzRect, Box, Sphere,
                    XzPolygon)
from camera import Camera

rows = 800
columns = 600
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

mat_mf_yellow = Microfacet(roughness=0.3,
                           albedo=ConstantTexture(Color(0.9, 0.9, 0.05)))
mat_mf_red = Microfacet(roughness=0.2,
                        albedo=ConstantTexture(Color(0.65, 0.05, 0.05)))
mat_mf_white = Microfacet(roughness=0.6,
                          albedo=ConstantTexture(Color(0.73, 0.73, 0.73)))
mat_mf_blue = Microfacet(roughness=0.15,
                         albedo=ConstantTexture(Color(0.05, 0.05, 0.73)))

mat_light = DiffuseLight(ConstantTexture(Color(15)))

# lights_list = [
#     FlipNormals(
#         XzPolygon([(204, 415), (189, 292), (348, 133), (366, 268)],
#                   554,
#                   mat_light,
#                   sample_type='uniform'))
# ]

lights_list = [
    FlipNormals(
        XzPolygon([(290, 431), (165, 330), (115, 212), (306, 125), (403, 220),
                   (381, 343)],
                  554,
                  mat_light,
                  sample_type='uniform'))
]

obj_list = [
    # wall
    FlipNormals(YzRect(0, 555, 0, 555, 555, mat_green)),
    YzRect(0, 555, 0, 555, 0, mat_red),
    FlipNormals(XzRect(0, 555, 0, 555, 555, mat_white)),
    XzRect(0, 555, 0, 555, 0, mat_white),
    FlipNormals(XyRect(0, 555, 0, 555, 555, mat_blue)),
    # Sphere
    Sphere(Point(420, 350, 80), 50, mat_mf_red),
    Sphere(Point(300, 200, 40), 20, mat_mf_blue),
    # box
    Translate(
        RotateX(RotateY(Box(Point(), Point(165, 165, 165), mat_mf_white), -45),
                -30), Vec3(130, 200, 65)),
    Translate(
        RotateZ(RotateY(Box(Point(), Point(165, 330, 165), mat_mf_yellow), 30),
                20), Vec3(265, 60, 295))
]

obj_list += lights_list

lights = HittableList(lights_list)
world = HittableList(obj_list)
