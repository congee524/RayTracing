import math


class Vec3():

    def __init__(self, *args):
        if len(args) == 0:
            self.x, self.y, self.z = (0.0, 0.0, 0.0)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (float, int)):
                self.x, self.y, self.z = (arg, arg, arg)
            elif isinstance(arg, (tuple, list)):
                assert len(arg) == 3, "Length of tuple or list must be 3!"
                self.x, self.y, self.z = arg
            elif isinstance(arg, Vec3):
                self.x, self.y, self.z = arg.x, arg.y, arg.z
            else:
                raise TypeError("Unsupported initialization parameters!")
        elif len(args) == 2:
            self.x, self.y, self.z = (args[0], args[1], 0.0)
        elif len(args) == 3:
            self.x, self.y, self.z = (args[0], args[1], args[2])
        else:
            raise TypeError("Vec3 accepts at most 3 params!")

        self.x, self.y, self.z = float(self.x), float(self.y), float(self.z)

    def __getitem__(self, key):
        assert isinstance(key, int), "index must be integer"
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("index out of range")

    def __setitem__(self, key, val):
        assert isinstance(key, int), "index must be integer"
        if isinstance(val, (float, int)):
            val = float(val)
        else:
            raise TypeError("Wrong type of value!")
        if key == 0:
            self.x = val
        elif key == 1:
            self.y = val
        elif key == 2:
            self.z = val
        else:
            raise IndexError("index out of range")

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(
                f"Unsupported operand type for +: {self.__class__} and {type(other)}"
            )

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            if hasattr(other, "__rmul__"):
                return other.__rmul__(self)
            else:
                raise TypeError("Unsupported operand type for *")

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError("Unsupported operand type for /")

    def __iadd__(self, other):
        if isinstance(other, Vec3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        else:
            raise TypeError("Unsupported operand type for +=")

    def __isub__(self, other):
        if isinstance(other, Vec3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            return self
        else:
            raise TypeError("Unsupported operand type for -=")

    def __imul__(self, other):
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            self.z *= other
            return self
        else:
            raise TypeError("Unsupported operand type for *=")

    def __itruediv__(self, other):
        if isinstance(other, (float, int)):
            self.x /= other
            self.y /= other
            self.z /= other
            return self
        else:
            raise TypeError("Unsupported operand type for /=")

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        if isinstance(other, Vec3):
            return math.isclose(self.x - other.x, 0.) and math.isclose(
                self.y - other.y, 0.) and math.isclose(self.z - other.z, 0.)
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return 3

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def square(self):
        return Vec3.dot(self, self)

    def length(self):
        return math.sqrt(self.square())

    @classmethod
    def dot(cls, v1, v2):
        if isinstance(v1, Vec3) and isinstance(v2, Vec3):
            return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
        else:
            raise TypeError("Unsupported operand type for dot()")

    @classmethod
    def cross(cls, v1, v2):
        if isinstance(v1, Vec3) and isinstance(v2, Vec3):
            return Vec3(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z,
                        v1.x * v2.y - v1.y * v2.x)
        else:
            raise TypeError("unsupported operand type for cross()")

    def normalize(self):
        length = self.length()
        return self / length

    def near_zero(self):
        return math.isclose(Vec3.dot(self, self), 0.)


class Point(Vec3):
    pass


class Color(Vec3):
    pass
