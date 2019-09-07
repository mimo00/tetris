import pygame
import sys

from tetris_design_patterns.core import R_CLOCKWISE, BLACK, Vector, DOWN, RIGHT, LEFT, Board, Block
from tetris_design_patterns.factory.classic_factory import ClassicTetrisBlockFactory
from tetris_design_patterns.gui import GUI

DROP_EVENT_ID = pygame.USEREVENT + 1


class TetrisApp(object):
    def __init__(self, rows=16, columns=10, board_color=BLACK, block_factory=ClassicTetrisBlockFactory()):
        self.rows = rows #number of X
        self.columns = columns #number of Y
        self.board_color = board_color
        self.block_factory = block_factory
        self.gameover = False
        self.paused = False
        self.board: Board = self.new_board()
        self.block: Block = self.new_block()
        self.gui = GUI(rows=self.rows, columns=self.columns)

    def new_board(self) -> Board:
        return [[self.board_color for _ in range(self.columns)] for _ in range(self.rows)]

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

    def move(self, point):
        if not self.gameover and not self.paused:
            new_block = self.block.get_moved(point)
            if not self.is_colliding(new_block):
                self.block = new_block

    def rotate(self, r=R_CLOCKWISE):
        if not self.gameover and not self.paused:
            new_block = self.block.get_rotated(r)
            if not self.is_colliding(new_block):
                self.block = new_block

    def quit(self):
        self.gui.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.gameover = False
            self.paused = False
            self.board = self.new_board()
            self.block = self.new_block()

    def remove_full_rows(self):
        for index, row in enumerate(self.board):
            if BLACK not in row:
                del self.board[index]
                self.board.insert(0, [self.board_color for _ in range(self.columns)])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == DROP_EVENT_ID:
                self.move(DOWN)
            elif event.type == pygame.QUIT:
                self.quit()
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
                    self.rotate(R_CLOCKWISE)
                elif event.key == pygame.K_p:
                    self.toggle_pause()
                elif event.key == pygame.K_SPACE:
                    self.start_game()

    def show_board(self):
        board = {Vector(x, y): self.board[x][y] for x in range(self.rows) for y in range(self.columns)}
        block = {point: self.block.color for point in self.block.points}
        self.gui.draw_shape(board)
        self.gui.draw_shape(block)

    def freeze_block(self):
        if self.is_colliding(self.block.get_moved(DOWN)):
            self.freeze_block_on_board()
            self.block = self.new_block()

    def check_game_over(self):
        for point in self.block.points:
            if point.x < 0:
                self.gameover=True

    def run(self):
        pygame.time.set_timer(DROP_EVENT_ID, 750)
        clock = pygame.time.Clock()

        while True:
            if self.gameover:
                self.gui.center_msg("Game Over! Press space to continue")
            elif self.paused:
                self.gui.center_msg("Paused")
            else:
                self.freeze_block()
                self.show_board()
                self.remove_full_rows()
                self.gui.refresh()
            self.handle_events()
            clock.tick(30)


if __name__ == '__main__':
    App = TetrisApp()
    App.run()
