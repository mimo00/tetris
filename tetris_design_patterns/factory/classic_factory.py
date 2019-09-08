import random

from tetris_design_patterns.core import Block, PURPLE, Vector, RED, GREEN
from tetris_design_patterns.factory.core import TetrisBlockFactory


class TBlock(Block):
    def __init__(self, color=PURPLE):
        points = [Vector(0, 0), Vector(0, 1), Vector(0, 2), Vector(1, 1)]
        center = Vector(1, 1)
        super().__init__(points, center, color)


class SBlock(Block):
    def __init__(self, color=RED):
        points = [Vector(0, 0), Vector(0, 1), Vector(-1, 1), Vector(-1, 2)]
        center = Vector(0, 1)
        super().__init__(points, center, color)


class IBlock(Block):
    def __init__(self, color=GREEN):
        points = [Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(3, 0)]
        center = Vector(1, 0)
        super().__init__(points, center, color)


class ClassicTetrisBlockFactory(TetrisBlockFactory):
    def create(self) -> Block:
        shape = random.randint(0, 2)
        if shape == 0:
            return TBlock()
        elif shape == 1:
            return SBlock()
        elif shape == 2:
            return IBlock()
