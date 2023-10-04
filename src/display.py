import pygame
import sys

class Chip8Display(object):
    def __init__(self):

        self.scale = 10

        # scale 64*32 screen
        self.height = 32
        self.width = 64
        
        self.white = (255,255,255)
        self.black = (0,0,0)

        pygame.init()

        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))

        pygame.display.set_caption('CHIP8')


    def flip_pixel(self, x,y) -> bool:
        """
        Returns: 
            0 if pixel was not set before, 1 if pixel was set
        """
        curr_pixel = self.screen.get_at((x * self.scale, y * self.scale))
        
        if(curr_pixel == (0,0,0)):
            new_color = (255,255,255)
            res = False
        else:
            new_color = (0,0,0)
            res = True
        pygame.draw.rect(self.screen, new_color, (x * self.scale, y * self.scale, self.scale, self.scale))
        return res

    def clear(self):
        self.screen.fill(self.white)

    def update(self):
        pygame.display.flip()