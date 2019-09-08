import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

import pygame
import sys

DROP_EVENT_ID = pygame.USEREVENT + 1

R_CLOCKWISE = ([0, 1], [-1, 0])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (218,112,214)


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
        r = R_CLOCKWISE
        point = self - pivot
        point = self.transform(r, point)
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


class GUI:
    def __init__(self, cell_size=20, rows=16, columns=8):
        self.cell_size = cell_size
        self.width = cell_size*columns
        self.height = cell_size*rows
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 12).render(
                line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))
            pygame.display.update()

    def draw_shape(self, board: Shape):
        for point, color in board.items():
            rect = (point.y * self.cell_size, point.x * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)

    def refresh(self):
        pygame.display.update()
        self.screen.fill((0, 0, 0))


class TetrisApp(object):
    def __init__(self, rows=16, columns=10, board_color=BLACK):
        self.rows = rows #number of X
        self.columns = columns #number of Y
        self.board_color = board_color
        self.gameover = False
        self.paused = False
        self.board: Board = self.new_board()
        self.block: Block = self.new_block()
        self.gui = GUI(rows=self.rows, columns=self.columns)

    def new_board(self) -> Board:
        return [[self.board_color for _ in range(self.columns)] for _ in range(self.rows)]

    def new_block(self):
        start_point = Vector(-2, self.columns//2)
        shape = random.randint(0, 2)
        block = TBlock()
        if shape == 0:
            block = TBlock()
        elif shape == 1:
            block = SBlock()
        elif shape == 2:
            block = IBlock()
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

    def rotate(self):
        if not self.gameover and not self.paused:
            new_block = self.block.get_rotated()
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
                    self.rotate()
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
