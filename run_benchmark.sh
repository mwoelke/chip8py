#!/bin/bash
if [ ! -e "roms/5-quirks.ch8" ]; then
wget -P $(pwd)/roms https://github.com/Timendus/chip8-test-suite/raw/adb1b383fe329f3de73a7caa4ac0af536ef8a179/bin/5-quirks.ch8
fi
./test_quirks.py