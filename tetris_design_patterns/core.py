from dataclasses import dataclass
from typing import Tuple, Dict, List

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

    def get_moved(self, point):
        return Vector(self.x + point.x, self.y + point.y)


DOWN = Vector(1, 0)
RIGHT = Vector(0, 1)
LEFT = Vector(0, -1)
Color = Tuple[int, int, int]
Shape = Dict[Vector, Color]
Board = List[List[Color]]


