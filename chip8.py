#!/usr/bin/env python3
from chip8.cpu import Chip8CPU
from chip8.display import Chip8Display
import pygame
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-r", "--rom", required=True, help="ROM to load")
parser.add_argument("-d", "--debug", help="Print debug information", action="store_true")
parser.add_argument("-w", "--wait", default=0, help="Sleep n ms between instructions (default 0)")
args = parser.parse_args()

screen = Chip8Display()
cpu = Chip8CPU(screen, args.debug)

# Timer for delay and sound timer.
# Chip8 expects timers to decrement at 60Hz which is ~17ms
TIMER_EVENT = pygame.USEREVENT
pygame.time.set_timer(TIMER_EVENT, 17)

# load font
with open('font.ch8', "rb") as font_file:
    rom = bytearray(font_file.read())
    cpu.load_memory(rom, 0x0)

# load ROM
with open(args.rom, "rb") as rom_file:
    rom = bytearray(rom_file.read())
    cpu.load_memory(rom, 0x200)

# main loop
while True:
    pygame.time.wait(int(args.wait))
    cpu.handle_events(pygame.event.get())
    cpu.execute_instr()