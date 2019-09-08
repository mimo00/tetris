import random

from tetris_design_patterns.core import PURPLE, Vector, RED, GREEN
from tetris_design_patterns.factory.core import TetrisBlockFactory, Block
from tetris_design_patterns.rotation_strategies import ClockwiseRotationStrategy, NoRotationStrategy


class TBlock(Block):
    def __init__(self, color=PURPLE):
        points = [Vector(0, 0), Vector(0, 1), Vector(0, 2), Vector(1, 1)]
        center = Vector(1, 1)
        super().__init__(points, center, color, ClockwiseRotationStrategy())


class SBlock(Block):
    def __init__(self, color=RED):
        points = [Vector(0, 0), Vector(0, 1), Vector(-1, 1), Vector(-1, 2)]
        center = Vector(0, 1)
        super().__init__(points, center, color, ClockwiseRotationStrategy())


class IBlock(Block):
    def __init__(self, color=GREEN):
        points = [Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(3, 0)]
        center = Vector(1, 0)
        super().__init__(points, center, color, ClockwiseRotationStrategy())


class OBlock(Block):
    def __init__(self, color=GREEN):
        points = [Vector(0, 0), Vector(1, 0), Vector(0, 1), Vector(1, 1)]
        center = Vector(1, 0)
        super().__init__(points, center, color, NoRotationStrategy())


class ClassicTetrisBlockFactory(TetrisBlockFactory):
    def create(self):
        shape = random.randint(0, 3)
        if shape == 0:
            return TBlock()
        elif shape == 1:
            return SBlock()
        elif shape == 2:
            return IBlock()
        elif shape == 3:
            return OBlock()
