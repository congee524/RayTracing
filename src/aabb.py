from vec import Vec3


def fmin(a, b):
    return a if a < b else b


def fmax(a, b):
    return a if a > b else b


class Aabb():

    def __init__(self, a, b):
        self._min = a
        self._max = b

    def hit(self, r, t_min, t_max):
        for i in range(3):
            div = 1.0 / r.direction[i]
            t1 = (self._min[i] - r.origin[i]) * div
            t2 = (self._max[i] - r.origin[i]) * div
            if div < 0.:
                t1, t2 = t2, t1
            t_min = t1 if t1 > t_min else t_min
            t_max = t2 if t2 < t_max else t_max
            if t_max <= t_min:
                return False

        return True

    def surrounding_box(box0, box1):
        if box0 is None:
            return box1
        if box1 is None:
            return box0
        small = Vec3([fmin(box0._min[i], box1._min[i]) for i in range(3)])
        big = Vec3([fmax(box0._max[i], box1._max[i]) for i in range(3)])
        return Aabb(small, big)
