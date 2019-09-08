from typing import List

from tetris_design_patterns.core import Vector, Color
from tetris_design_patterns.rotation_strategies import RotationStrategy


class Block:
    def __init__(self, points, center, color, rotation_strategy):
        self.points: List[Vector] = points
        self.center = center
        self.color: Color = color
        self.rotation_strategy: RotationStrategy = rotation_strategy

    def get_rotated(self):
        points = []
        for point in self.points:
            new_point = self.rotation_strategy.get_rotated(point, self.center)
            points.append(new_point)
        return Block(points, self.center, self.color, self.rotation_strategy)

    def get_moved(self, point):
        points = []
        for p in self.points:
            points.append(p.get_moved(point))
        return Block(points, self.center.get_moved(point), self.color, self.rotation_strategy)


class TetrisBlockFactory:
    def create(self) -> Block:
        raise NotImplementedError
