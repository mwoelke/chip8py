#!/usr/bin/python3
from chip8.display import Chip8Display
import pygame


display = Chip8Display()

data = [
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000111111111111100000000000000000000000000000000000000000000000',
    '0000111111111111100000000000000000000000000000000000000000000000',
    '0000000001100000000000000000000000000000000000000000000000000000',
    '0000000001100000000000000000000000000000000000000000000000000000',
    '0000000001100000111111111111110000000000000000000000000000000000',
    '0000000001100000111111111111110000000000000000000000000000000000',
    '0000000001100000110000000000000000000000000000000000000000000000',
    '0000000001100000110000000000000000000000000000000000000000000000',
    '0000000001100000110000000000000000000000000000000000000000000000',
    '0000000001100000111111111111110001111111111110000000000000000000',
    '0000000001100000111111111111110001111111111110000000000000000000',
    '0000000000000000110000000000000001110000000000000000000000000000',
    '0000000000000000110000000000000001110000000000000000000000000000',
    '0000000000000000110000000000000001111111111110000000000000000000',
    '0000000000000000110000000000000001111111111110000000000000000000',
    '0000000000000000111111111111110000000000001110000000000000000000',
    '0000000000000000111111111111110000000000001110011111111111100000',
    '0000000000000000000000000000000001111111111110011111111111100000',
    '0000000000000000000000000000000001111111111110000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000110000000000',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000000000000000000000000000000000000000000000000000'
]

for y, row in enumerate(data):
    for x, char in enumerate(row):
        if char == '1':
            display.flip_pixel(x,y)

display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()