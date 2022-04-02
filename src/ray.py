from vec import Vec3, Point


class Ray():

    def __init__(self, orig, dir, t=0.):
        self.origin = orig
        self.direction = dir
        self.time = t

    def at(self, t):
        return self.origin + t * self.direction
