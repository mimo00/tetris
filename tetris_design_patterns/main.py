import pygame
import sys

from tetris_design_patterns.core import BLACK, Vector, DOWN, RIGHT, LEFT, Board
from tetris_design_patterns.factory.core import Block
from tetris_design_patterns.factory.classic_factory import ClassicTetrisBlockFactory, OBlock
from tetris_design_patterns.gui import GUI

DROP_EVENT_ID = pygame.USEREVENT + 1


class TetrisApp(object):
    def __init__(self, rows=16, columns=10, board_color=BLACK, block_factory=ClassicTetrisBlockFactory()):
        self.gui = GUI(rows=rows, columns=columns)
        self.state = GameState(self.gui, rows, columns, board_color, block_factory)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            try:
                self.state.handle()
            except ChangeStateException as e:
                self.state = e.new_state
            clock.tick(30)


class ChangeStateException(Exception):
    def __init__(self, new_state) -> None:
        self.new_state = new_state


class TetrisState:
    def __init__(self, gui):
        self.gui = gui
        super().__init__()

    def handle(self):
        raise NotImplementedError


class GameOverState(TetrisState):
    def __init__(self, gui, game_state):
        super().__init__(gui)
        self.game_state = game_state

    def handle(self):
        self.gui.center_msg("Game Over! Press space to continue")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_game = GameState(
                        self.gui, self.game_state.rows, self.game_state.columns,
                        self.game_state.board_color, self.game_state.block_factory)
                    raise ChangeStateException(new_game)


class PausedState(TetrisState):
    def __init__(self, gui, game_state):
        super().__init__(gui)
        self.game_state = game_state

    def handle(self):
        self.gui.center_msg("Paused")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    raise ChangeStateException(self.game_state)


class GameState(TetrisState):
    def __init__(self, gui, rows, columns, board_color, block_factory):
        self.rows = rows #number of X
        self.columns = columns #number of Y
        self.board_color = board_color
        self.block_factory = block_factory
        self.board: Board = self.new_board()
        self.block: Block = self.new_block()
        pygame.time.set_timer(DROP_EVENT_ID, 750)
        super().__init__(gui)

    def new_board(self) -> Board:
        return [[self.board_color for _ in range(self.columns)] for _ in range(self.rows)]

    def move(self, point):
        new_block = self.block.get_moved(point)
        if not self.is_colliding(new_block):
            self.block = new_block

    def rotate(self):
        new_block = self.block.get_rotated()
        if not self.is_colliding(new_block):
            self.block = new_block

    def new_block(self):
        start_point = Vector(-2, self.columns // 2)
        block = self.block_factory.create()
        block = block.get_moved(start_point)
        if self.is_colliding(block):
            self.check_game_over()
        return block

    def is_colliding(self, block):
        for point in block.points:
            if point.x >= self.rows:
                return True
            if point.y < 0 or point.y >= self.columns:
                return True
            if point.x >= 0 and self.board[point.x][point.y] != BLACK:
                return True
        return False

    def freeze_block_on_board(self):
        for point in self.block.points:
            self.board[point.x][point.y] = self.block.color

    def show_board(self):
        board = {Vector(x, y): self.board[x][y] for x in range(self.rows) for y in range(self.columns)}
        block = {point: self.block.color for point in self.block.points}
        self.gui.draw_shape(board)
        self.gui.draw_shape(block)

    def freeze_block(self):
        if self.is_colliding(self.block.get_moved(DOWN)):
            self.freeze_block_on_board()
            self.block = self.new_block()

    def remove_full_rows(self):
        for index, row in enumerate(self.board):
            if BLACK not in row:
                del self.board[index]
                self.board.insert(0, [self.board_color for _ in range(self.columns)])

    def check_game_over(self):
        for point in self.block.points:
            if point.x < 0:
                raise ChangeStateException(GameOverState(self.gui, self))

    def quit(self):
        self.gui.center_msg("Exiting...")
        sys.exit()

    def handle(self):
        self.freeze_block()
        self.show_board()
        self.remove_full_rows()
        self.gui.refresh()

        for event in pygame.event.get():
            if event.type == DROP_EVENT_ID:
                self.move(DOWN)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_LEFT:
                    self.move(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.move(RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.move(DOWN)
                elif event.key == pygame.K_UP:
                    self.rotate()
                elif event.key == pygame.K_p:
                    raise ChangeStateException(PausedState(self.gui, self))


if __name__ == '__main__':
    App = TetrisApp()
    App.run()
