from dataclasses import dataclass
from typing import Tuple, Dict, List

R_CLOCKWISE = ([0, 1], [-1, 0])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (218,112,214)
YELLOW = (255, 255, 0)


@dataclass
class Vector:
    x: int
    y: int

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Vector):
            return self.x == o.x and self.y == o.y
        return False

    def get_rotated(self, pivot):
        R = R_CLOCKWISE
        point = self - pivot
        point = self.transform(R, point)
        point = pivot + point
        return point

    def get_moved(self, point):
        return Vector(self.x + point.x, self.y + point.y)

    @staticmethod
    def transform(r, point):
        x = r[0][0] * point.x + r[0][1] * point.y
        y = r[1][0] * point.x + r[1][1] * point.y
        return Vector(x, y)


DOWN = Vector(1, 0)
RIGHT = Vector(0, 1)
LEFT = Vector(0, -1)
Color = Tuple[int, int, int]
Shape = Dict[Vector, Color]
Board = List[List[Color]]


class Block:
    def __init__(self, points, center, color):
        self.points: List[Vector] = points
        self.center: Vector = center
        self.color: Color = color

    def get_rotated(self):
        points = []
        for point in self.points:
            points.append(point.get_rotated(self.center))
        return Block(points, self.center, self.color)

    def get_moved(self, point):
        points = []
        for p in self.points:
            points.append(p.get_moved(point))
        return Block(points, self.center.get_moved(point), self.color)
