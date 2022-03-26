from vec import Vec3, Point


class Ray():

    def __init__(self, origin, direction):
        if not (isinstance(origin, Point) and isinstance(direction, Vec3)):
            raise TypeError("origin & direction must be Point & Vec3")

        self.orig = origin
        self.dir = direction

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def at(self, t):
        return self.orig + t * self.dir
