import pygame
import sys

COLOR_OFF = (0, 0, 0)
COLOR_ON = (255, 255, 255)
SCALE = 10


class Chip8Display(object):
    def __init__(self):
        # 64 * 32 screen
        self.width = 64
        self.height = 32

        pygame.init()

        self.screen = pygame.display.set_mode((self.width * SCALE, self.height * SCALE))

        pygame.display.set_caption("CHIP8")

    def flip_pixel(self, x, y) -> bool:
        """
        Flip the pixel at coordinate (x,y)

        :returns:
            0 if pixel was not set before, 1 if pixel was set
        """
        curr_pixel = self.screen.get_at((x * SCALE, y * SCALE))

        if curr_pixel == COLOR_OFF:
            new_color = COLOR_ON
            res = False
        else:
            new_color = COLOR_OFF
            res = True
        pygame.draw.rect(self.screen, new_color, (x * SCALE, y * SCALE, SCALE, SCALE))
        return res

    def clear(self):
        self.screen.fill(COLOR_OFF)

    def update(self):
        pygame.display.flip()
