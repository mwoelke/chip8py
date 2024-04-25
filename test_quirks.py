#!/usr/bin/env python3
from chip8.cpu import Chip8CPU
from chip8.display import Chip8Display
from timeit import default_timer as timer
import pygame

screen = Chip8Display()
cpu = Chip8CPU(screen, False)
cpu.memory[0x1ff] = 1

# Timer for delay and sound timer.
# Chip8 expects timers to decrement at 60Hz which is ~17ms
TIMER_EVENT = pygame.USEREVENT
pygame.time.set_timer(TIMER_EVENT, 17)

# load font
with open('font.ch8', "rb") as font_file:
    rom = bytearray(font_file.read())
    cpu.load_memory(rom, 0x0)

# load ROM
with open('roms/5-quirks.ch8', "rb") as rom_file:
    rom = bytearray(rom_file.read())
    cpu.load_memory(rom, 0x200)

# run for exactly 75,502 instructions
start = timer()
for i in range(75_502):
    #pygame.time.wait(int(args.wait))
    cpu.handle_events(pygame.event.get())
    cpu.execute_instr()
end = timer()
print(f"Quirks test took {end - start}s")