import pygame

COLOR_OFF = (0xff, 0xf6, 0xd3)
COLOR_ON  = (0x7c, 0x3f, 0x58)
SCALE = 10

class Chip8Display(object):
    def __init__(self):
        # 64 * 32 screen
        self.width = 64
        self.height = 32

        pygame.init()

        self.screen_state = [ [0]*self.height for _ in range(self.width)]

        self.screen = pygame.display.set_mode((self.width * SCALE, self.height * SCALE))
        self.screen.fill(COLOR_ON)

        pygame.display.set_caption("CHIP8")

    def flip_pixel(self, x, y) -> bool:
        """
        Flip the pixel at coordinate (x,y)

        :returns:
            0 if pixel was not set before, 1 if pixel was set
        """
        curr_pixel = self.screen_state[x][y]

        if curr_pixel == 0:
            new_color = COLOR_ON
            self.screen_state[x][y] = 1
            res = False
        else:
            new_color = COLOR_OFF
            self.screen_state[x][y] = 0
            res = True
        pygame.draw.rect(self.screen, new_color, (x * SCALE, y * SCALE, SCALE, SCALE))
        return res

    def clear(self):
        self.screen_state = [ [0]*self.height for _ in range(self.width)]
        self.screen.fill(COLOR_OFF)

    def update(self):
        pygame.display.flip()
