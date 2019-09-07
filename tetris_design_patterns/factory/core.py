from tetris_design_patterns.core import Block


class TetrisBlockFactory:
    def create(self) -> Block:
        raise NotImplementedError
