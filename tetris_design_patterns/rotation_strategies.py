from basic import Vector


class RotationStrategy:
    def get_rotated(self, point: Vector, center: Vector) -> Vector:
        raise NotImplementedError


class NoRotationStrategy(RotationStrategy):
    def get_rotated(self, point: Vector, center: Vector) -> Vector:
        return point


class ClockwiseRotationStrategy(RotationStrategy):
    def get_rotated(self, point: Vector, center: Vector) -> Vector:
        r = ([0, 1], [-1, 0])
        point = point - center
        point = self.transform(r, point)
        point = center + point
        return point

    @staticmethod
    def transform(r, point):
        x = r[0][0] * point.x + r[0][1] * point.y
        y = r[1][0] * point.x + r[1][1] * point.y
        return Vector(x, y)
