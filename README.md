# chip8py
My take on a chip8 interpreter in python.

Although this is a work in progress, it should handle some ROMs somewhat fine by now.

**Note**: Chip8 is a bit of a weird plattform given it's different implementations with their own quirks. This specific implementation only handles the original chip8.

# Usage

```
./chip8.py -r ROM_PATH [-h/--help] [-d/--debug]
```

# Setup

`Pygame` is the sole dependency. If not installed, run `pip install -r requirements.txt`.

Developed/tested against Python 3.11, however lower versions might work as well.


# References
Big shoutouts to the following articles / posts / repos:

https://tobiasvl.github.io/blog/write-a-chip-8-emulator - Great reference overall

http://devernay.free.fr/hacks/chip8/C8TECH10.HTM - Used this for implementing the opcodes and other technical stuff

https://github.com/craigthomas/Chip8Python - Really nice emulator which I took much inspiration from

https://github.com/corax89/chip8-test-rom - For providing a test ROM

https://github.com/Timendus/chip8-test-suite - For providing a whole test suite
