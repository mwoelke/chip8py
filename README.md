# chip8py

My take on a chip8 interpreter in python.

This should handle most ROMs fine. If games run too fast, run them with a delay (see below).

**Note**: Chip8 is a bit of a weird plattform given it's different implementations with their own quirks. This specific implementation only handles the original chip8.

# Usage

```
chip8.py [-h] -r ROM [-d] [-w WAIT]

options:
  -h, --help            show this help message and exit
  -r ROM, --rom ROM     ROM to load
  -d, --debug           Print debug information
  -w WAIT, --wait WAIT  Sleep n ms between instructions (default 0)
```

# Setup

`Pygame` is the sole dependency. If not installed, run `pip install -r requirements.txt`.

Developed/tested against Python 3.11, however lower versions might work as well.

## Note on sound

The chip8 only knows one beep sound. I find it rather annoying and doesn't add much value, which is why I didn't include one.
You may add your favorite beep sound as 'sound.wav' to the root directory and it will be used.

# Benchmark

Run `./run_benchmark.sh` to run a benchmark. Automatically downloads required ROMs. 

This exists mostly for me to iterate over different ideas to make things more efficient.

# References
Big shoutouts to the following articles / posts / repos:

https://tobiasvl.github.io/blog/write-a-chip-8-emulator - Great reference overall

http://devernay.free.fr/hacks/chip8/C8TECH10.HTM - Used this for implementing the opcodes and other technical stuff

https://github.com/craigthomas/Chip8Python - Really nice emulator which I took much inspiration from

https://github.com/corax89/chip8-test-rom - For providing a test ROM

https://github.com/Timendus/chip8-test-suite - For providing a whole test suite
