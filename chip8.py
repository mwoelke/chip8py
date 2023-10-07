#!/usr/bin/python3
from chip8.cpu import Chip8CPU
from chip8.display import Chip8Display
import pygame
import sys

screen = Chip8Display()
cpu = Chip8CPU(screen)

with open("roms/IBM_Logo.ch8", "rb") as rom_file:
    rom = bytearray(rom_file.read())
    cpu.load_memory(rom, 0x200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    cpu.execute_instr()
