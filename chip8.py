#!/usr/bin/python3
from chip8.cpu import Chip8CPU
from chip8.display import Chip8Display
import pygame
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-r", "--rom", required=True, help="ROM to load")
parser.add_argument("-d", "--debug", help="Print debug information", action="store_true")
args = parser.parse_args()

screen = Chip8Display()
cpu = Chip8CPU(screen, args.debug)

# Timer for delay and sound timer.
# Chip8 expects timers to decrement at 60Hz which is ~17ms
TIMER_EVENT = pygame.USEREVENT
pygame.time.set_timer(TIMER_EVENT, 17)

# load ROM
with open(args.rom, "rb") as rom_file:
    rom = bytearray(rom_file.read())
    cpu.load_memory(rom, 0x200)

# main loop
while True:
    pygame.time.wait(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == TIMER_EVENT:
            cpu.decrement_timers()
    cpu.execute_instr()