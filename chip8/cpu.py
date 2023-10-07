from chip8.cpu_exception import OpcodeNotImplementedException
from chip8.display import Chip8Display
from random import randint
from math import floor

MEMORY_SIZE = 4069

class Chip8CPU:
    def __init__(self, display: Chip8Display, debug: bool = False):
        self.display = display
        self.debug = debug

        # initialize the 16 general purpose registers (v0 - vF) (8 bit)
        self.v = []
        # fill v registers with 0 on boot
        for currRegister in range(0xF + 1):
            self.v.append(0x0)

        # initialize I register (16 bit)
        self.I = 0x0

        # initialize program counter (16 bit)
        self.pc = 0x200

        # initialize stack pointer (8 bit)
        # self.sp = 0x0
        # is this needed?

        # initialize stack (should be 16 x 16 bit)
        self.stack = []

        # initialize timers
        self.timers = {"delay": 0x0, "sound": 0x0}

        # current operand
        self.operand = 0x0

        # initialize RAM
        self.memory = bytearray(MEMORY_SIZE)

    # execute next instruction
    def execute_instr(self):
        self.operand = (
            self.memory[self.pc] << 8
        )  # get first byte of next instruction from memory
        self.operand += self.memory[
            self.pc + 1
        ]  # get second byte of next instruction from memory

        # split operand into nibbles
        operand_nibbles = (
            (self.operand & 0xF000) >> 12,
            (self.operand & 0x0F00) >> 8,
            (self.operand & 0x00F0) >> 4,
            (self.operand & 0x000F),
        )

        if self.debug:
            print('-----')
            print(f"Executing: {hex(operand_nibbles[0]), hex(operand_nibbles[1]), hex(operand_nibbles[2]), hex(operand_nibbles[3])}")
            print(f"PC: {self.pc}")

        # decode and execute
        match operand_nibbles:
            case (0x0, 0x0, 0xE, 0x0):  # 00E0 (clear screen)
                self.instr_cls()
            case (0x0, 0x0, 0xE, 0xE):  # 00EE (return from subroutine)
                self.instr_ret()
            case (0x1, _, _, _):        # 1xxx (jump)
                self.instr_jmp()
                return # Do not increment pc
            case (0x2, _, _, _):        # 2xxx (call subroutine)
                self.instr_call()
            case (0x3, _, _, _):        # 3xyy (skip if Vx == yy)
                self.instr_se_vx_byte()
            case (0x4, _, _, _):        # 4xyy (skip if Vx != yy)
                self.instr_sne_vx_byte()        
            case (0x5, _, _, 0):        # 5xy0 (skip if Vx == Vy)
                self.instr_se_vx_vy()
            case (0x6, _, _, _):        # 6xyy (Vx == yy)
                self.instr_ld_byte()
            case (0x7, _, _, _):        # 7xyy (Vx += yy)
                self.instr_add_byte()
            case (0x8, _, _, 0x0):      # 8xy0 (Vx = Vy)
                self.instr_ld_vx_vy()
            case (0x8, _, _, 0x1):      # 8xy1 (Vx OR Vy)
                self.instr_or_vx_vy()
            case (0x8, _, _, 0x2):      # 8xy2 (Vx AND Vy)
                self.instr_and_vx_vy()
            case (0x8, _, _, 0x3):      # 8xy3 (Vx XOR Vy)
                self.instr_xor_vx_vy()
            case (0x8, _, _, 0x4):      # 8xy4 (Vx += Vy) 
                self.instr_add_vx_vy()
            case (0x8, _, _, 0x5):      # 8xy5 (Vx -= Vy)
                self.instr_sub_vx_vy()
            case (0x8, _, _, 0x6):      # 8xy6 (shift-right Vx)
                self.instr_shr_vx()
            case (0x8, _, _, 0xE):      # 8xyE (shift-left Vx)
                self.instr_shl_vx()
            case (0x9, _, _, 0x0):      # 9xy0 (skip if Vx != Vy)
                self.instr_sne_vx_vy()
            case (0xA, _, _, _):        # Axxx (I = xxx)
                self.instr_ld_i_byte()
            case (0xC, _, _, _):        # Cxyy (Vx = random)
                self.instr_vx_rnd()
            case (0xD, _, _, _):        # Dxyz (draw)
                self.instr_drw()
            case (0xF, _, 0, 7):        # Fx07 (Vx = delay timer)
                self.instr_ld_vx_dt()
            case (0xF, _, 0x1, 0x5):    # Fx15 (delay timer = Vx)
                self.instr_ld_dt_vx()
            case (0xF, _, 0x1, 0xE):    # Fx1E (I += Vx)
                self.instr_add_i_vx()
            case (0xF, _, 0x2, 0x9):    # Fx29 (Load sprite for nibble at Vx) 
                self.instr_ld_i_vx()
            case (0xF, _, 0x3, 0x3):    # Fx33 (Store decimal number at I)
                self.instr_ld_bcd_vx_i()
            case (0xF, _, 0x5, 0x5):    # Fx55 (Store V0 to Vx starting at I)
                self.instr_store_v0_vx()
            case (0xF, _, 0x6, 0x5):    # Fx65 (Read V0 to Vx starting at I)
                self.instr_read_v0_vx()
            case _:  # unknown opcode, raise exception
                raise OpcodeNotImplementedException((operand_nibbles, self.pc - 0x200))

        self.pc += 2  # increment program counter by two bytes

    def load_memory(self, memory: bytearray, offset: int):
        """
        Load bytearray into memory at given offset.
        ROMs should go at 0x200.
        """
        if (
            len(memory) + offset
        ) > MEMORY_SIZE:  # throw exception when loading too much into memory
            raise Exception(f"Memory limit of {MEMORY_SIZE} exceeded")
        for index, value in enumerate(memory):
            self.memory[index + offset] = value

    def decrement_timers(self):
        """
        Decrease delay and sound timer by one
        """
        # print(f"Delay: {self.timers['delay']} | Sound: {self.timers['sound']}")
        if self.timers['delay'] > 0:
            self.timers['delay'] -= 1
        if self.timers['sound'] > 0:
            self.timers['sound'] -= 1

    ###################
    ### CPU opcodes ###
    ###################

    def instr_cls(self):
        """
        00E0: Clear display
        """
        self.display.clear()

    # 00EE: Return from subroutine
    def instr_ret(self):
        """
        00EE: Return from subroutine
        """
        self.pc = self.stack.pop()
        # self.sp -= 1

    def instr_jmp(self):
        """
        1xxx: Set program counter to xxx
        """
        self.pc = self.operand & 0x0FFF

    def instr_call(self):
        """
        2xxx: Call subroutine. 
        Put current PC on top of stack and set PC to xxx
        """
        self.stack.append(self.pc)
        self.pc = self.operand & 0x0FFF

    def instr_se_vx_byte(self):
        """
        3xyy: Skip next instruction if Vx = yy (increment pc by 2)
        """
        x = (self.operand & 0x0F00) >> 8
        yy = self.operand & 0x00FF
        if self.v[x] == yy:
            self.pc += 2

    def instr_sne_vx_byte(self):
        """
        4xyy: Skip next instruction if Vx != yy (increment pc by 2)
        """
        x = (self.operand & 0x0F00) >> 8
        yy = self.operand & 0x00FF
        if self.v[x] != yy:
            self.pc += 2

    def instr_se_vx_vy(self):
        """
        5xy0: Skip next instruction if Vx = Vy (increment pc by 2)
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        if self.v[x] == self.v[y]:
            self.pc += 2

    # 6xyy: Vx = yy
    def instr_ld_byte(self):
        x = (self.operand & 0x0F00) >> 8
        self.v[x] = self.operand & 0x00FF

    # 7xyy: Vx += yy
    def instr_add_byte(self):
        x = (self.operand & 0x0F00) >> 8
        self.v[x] += (self.operand & 0x00FF) 
        if self.v[x] > 255:  # handle overflow (8-bit).
            self.v[x] -= 256

    def instr_ld_vx_vy(self):
        """
        8xy0: Vx = Vy
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] = self.v[y]

    def instr_or_vx_vy(self):
        """
        8xy1: Vx OR Vy, store result in Vx
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] |= self.v[y]

    def instr_and_vx_vy(self):
        """
        8xy2: Vx AND Vy, store result in Vx
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] &= self.v[y]

    def instr_xor_vx_vy(self):
        """
        8xy3: Vx XOR Vy, store result in Vx
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] = self.v[x] ^ self.v[y]

    def instr_add_vx_vy(self):
        """
        8xy4: Vx += Vy, set Vf = 1 on overflow or Vf = 0 otherwise
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] += self.v[y]

        if self.v[x] > 255:  # handle overflow
            self.v[x] -= 256
            self.v[0xF] = 1
        else:
            self.v[0xF] = 0

    def instr_sub_vx_vy(self):
        """
        8xy5: Vx -= Vy, set Vf = 1 if Vx > Vy or Vf = 0 otherwise
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] -= self.v[y]
        if self.v[x] < 0:
            self.v[x] += 256
            self.v[0xF] = 0
        else:
            self.v[0xF] = 1

    def instr_shr_vx(self):
        """
        8xy6: Vx = Vy, then right-shift Vx by 1 
        Set Vf = 1 if least-significant bit of Vx was 1 or Vf = 0 otherwise.
        WARNING: This opcode is ambiguous! Many Chip-8 implementations ignore Vy.
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] = self.v[y]
        self.v[0xF] = self.v[x] & 0x1
        self.v[x] >>= 1
        

    # 8xy7: Subtract Vx from Vy and store on Vx. Set Vf = 1 if Vx > Vy or Vf = 0 otherwise
    def instr_subn_vy(self):
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] = self.v[y] - self.v[x]
        if self.v[x] < 0:
            self.v[x] += 256
            self.v[0xF] = 0
        else:
            self.v[0xF] = 1

    def instr_shl_vx(self):
        """
        8xyE: Vx = Vy, then left-shift Vx by 1 
        Set Vf = 1 if most-significant bit of Vx was 1 or Vf = 0 otherwise.
        WARNING: This opcode is ambiguous! Many Chip-8 implementations ignore Vy.
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        self.v[x] = self.v[y]
        self.v[0xF] = self.v[x] & 0x80
        self.v[x] <<= 1

    def instr_sne_vx_vy(self):
        """
        9xy0: Skip next instruction if Vx != Vy (increment pc by 2)
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        if self.v[x] != self.v[y]:
            self.pc += 2

    def instr_ld_i_byte(self):
        """
        I = xxx
        """
        self.I = self.operand & 0x0FFF

    # Bxxx: Program counter is set to xxx + V0.
    # Note: Apparently this is not widely used and behaviour is different on SUPER-CHIP
    def instr_jp_v0(self):
        self.pc = (self.operand & 0x0FFF) + self.v[0]

    def instr_vx_rnd(self):
        """
        Cxyy: Set Vx to a random byte AND yy
        """
        x = (self.operand & 0x0F00) >> 8
        rand = randint(0, 255)
        self.v[x] = rand & (self.operand & 0x00FF)

    def instr_drw(self):
        """
        Dxyz: Display z-byte sprite starting from I at (Vx, Vy). 
        Set Vf = 1 if a already drawn pixel gets overwritten (XOR).
        """
        x = (self.operand & 0x0F00) >> 8
        y = (self.operand & 0x00F0) >> 4
        z = self.operand & 0x000F

        x_pos = self.v[x] % 64
        y_pos = self.v[y] % 32

        if self.debug: 
            print(f"Printing sprite at ({(x_pos, y_pos)})")

        self.v[0xF] = 0  # reset Vf
        for row in range(z):
            sprite_row = self.memory[self.I + row]  # get byte to display at current row

            # split into individual pixels (note: string manipulation might be faster)
            pixels = [
                (sprite_row & 0x80) >> 7,
                (sprite_row & 0x40) >> 6,
                (sprite_row & 0x20) >> 5,
                (sprite_row & 0x10) >> 4,
                (sprite_row & 0x8) >> 3,
                (sprite_row & 0x4) >> 2,
                (sprite_row & 0x2) >> 1,
                (sprite_row & 0x1),
            ]

            if self.debug:
                print(f"Trying to print sprite from ({hex(self.I + row)}): {pixels}")

            for index, pixel in enumerate(pixels):
                if pixel == 1:
                    x_coord = (x_pos + index)
                    y_coord = (y_pos + row)
                    if x_coord >= 64 or y_coord >= 32:
                        break
                    if self.display.flip_pixel(x_coord, y_coord):
                        self.v[0xF] = 1

        self.display.update()  # update screen

    # Ex9E: Skip next instruction if key with value of Vx is pressed
    def instr_skp(self):
        raise OpcodeNotImplementedException("skip next if key vx is pressed")

    # ExA1: Skip next instruction if key with value of Vx is not pressed
    def instr_sknp(self):
        raise OpcodeNotImplementedException("skip next if key vx is not pressed")

    def instr_ld_vx_dt(self):
        """
        Fx07: Vx = delay timer
        """
        x = (self.operand & 0x0F00) >> 8
        self.v[x] = self.timers["delay"]

    # Fx0A: Stop execution until key is pressed, then store value of key in Vx
    def instr_ld_vx_k(self):
        raise OpcodeNotImplementedException()
        x = (self.operand & 0x0F00) >> 8
        k = 0xA  # @todo: get key here
        self.v[x] = k

    def instr_ld_dt_vx(self):
        """
        Fx15: Delay timer = Vx
        """
        x = (self.operand & 0x0F00) >> 8
        self.timers["delay"] = self.v[x]

    # Fx18: Sound timer = Vx
    def instr_ld_vx_st(self):
        x = (self.operand & 0x0F00) >> 8
        self.timers["delay"] = self.v[x]

    def instr_add_i_vx(self):
        """
        Fx1E: I = I + Vx
        """
        x = (self.operand & 0x0F00) >> 8
        self.I += self.v[x]  # @todo: overflow?

    def instr_ld_i_vx(self):
        """
        Fx29: I = Location of sprite for digit Vx
        """
        x = (self.operand & 0x0F00) >> 8
        self.I = self.v[x] * 10

    def instr_ld_bcd_vx_i(self):
        """
        Fx33: Take decimal number in format 'abc' from Vx and store a at I, b at I+1 and c at I+2
        """
        x = (self.operand & 0x0F00) >> 8

        a = floor(self.v[x] / 100)
        b = self.v[x] % 100
        b = floor(b / 10)
        c = self.v[x] % 10

        self.memory[self.I] = int(a)  # are int checks required?
        self.memory[self.I + 1] = int(b)
        self.memory[self.I + 2] = int(c)

    def instr_store_v0_vx(self):
        """
        Fx55: Store v0 to Vx in memory starting at address in I
        """
        x = (self.operand & 0x0F00) >> 8

        for i in range(x + 1):
            self.memory[self.I + i] = self.v[i]

    def instr_read_v0_vx(self):
        """
        Fx65: Read v0 to Vx from memory starting at address in I
        """
        x = (self.operand & 0x0F00) >> 8

        for i in range(x + 1):
            self.v[i] = self.memory[self.I + i]
