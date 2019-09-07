import pygame

from tetris_design_patterns.core import Shape


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
