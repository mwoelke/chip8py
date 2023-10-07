from cpu_exception import OpcodeNotImplementedException
from random import randint
from math import floor
from display import Chip8Display

MEMORY_SIZE = 4069

class Chip8CPU:
    def __init__(self, display: Chip8Display):

        self.display = display

        # initialize the 16 general purpose registers (v0 - vF) (8 bit)
        self.v = []
        # fill v registers with 0 on boot
        for currRegister in range(0xf + 1):
            self.v.append(0x0)

        # initialize I register (16 bit)
        self.I = 0x0

        # initialize program counter (16 bit)
        self.pc = 0x200

        # initialize stack pointer (8 bit)
        #self.sp = 0x0 
        # is this needed?

        # initialize stack (should be 16 x 16 bit)
        self.stack = []

        # initialize timers
        self.timers = {
            'delay': 0x0,
            'sound': 0x0
        }
    
        # current operand
        self.operand = 0x0

        # initialize RAM
        self.memory = bytearray(MEMORY_SIZE)


    # execute next instruction
    def execute_instr(self):
        
        self.operand = self.memory[self.pc] << 8 # get first byte of next instruction from memory
        self.operand += self.memory[self.pc + 1] # get second byte of next instruction from memory
        
        # split operand into nibbles
        operand_nibbles = (
            (self.operand & 0xf000) >> 12,
            (self.operand & 0x0f00) >> 8,
            (self.operand & 0x00f0) >> 4,
            (self.operand & 0x000f)
        )

        #print('-----')
        #print(f"Executing: {hex(operand_nibbles[0]), hex(operand_nibbles[1]), hex(operand_nibbles[2]), hex(operand_nibbles[3])}")
        #print(f"PC: {self.pc}")

        advance = True

        # decode and execute
        match operand_nibbles:
            case (0x0, 0x0, 0xe, 0x0): # 00E0 (clear screen)
                self.instr_cls()
            case (0x0, 0x0, 0xe, 0xe): # 00EE (return from subroutine)
                self.instr_ret()
            case (0x1, _, _, _):       # 1xxx (jump, pc = xxx)
                self.instr_jmp()
                advance = False
            case (0x6, _, _, _):       # 6xyy (Vx == yy)
                self.instr_ld_byte()   
            case (0x7, _, _, _):       # 7xyy (Vx += yy)
                self.instr_add_byte()   
            case (0xa, _, _, _):       # Axxx (I = xxx)
                self.instr_ld_i()
            case (0xd, _, _, _):       # Dxyz (draw)
                self.instr_drw()           
            case _: # unknown opcode, raise exception
                raise OpcodeNotImplementedException((operand_nibbles, self.pc - 0x200))

        if advance:
            self.pc += 2 # increment program counter by two bytes

    # load bytearray into memory and add padding if required
    def load_memory(self, memory: bytearray, offset: int):
        if (len(memory) + offset) > MEMORY_SIZE: # throw exception when loading too much into memory
            raise Exception(f'Memory limit of {MEMORY_SIZE} exceeded')
        for index, value in enumerate(memory):
            self.memory[index + offset] = value

    ###################
    ### CPU opcodes ###
    ###################

    # 00E0: Clear display
    def instr_cls(self):
        self.display.clear()
    
    # 00EE: Return from subroutine
    def instr_ret(self): 
        self.pc = self.stack.pop()
        #self.sp -= 1
    
    # 1xxx: Set program counter to xxx
    def instr_jmp(self):
        self.pc = self.operand & 0x0fff

    # 2xxx: Call subroutine. Puts current pc on top of stack and set pc to 2xxx
    def instr_call(self):
        #self.sp += 1
        self.stack.append(self.pc)
        self.pc = self.operand & 0x0fff

    # 3xyy: Skip next instruction if Vx = yy (increment pc by 2)
    def instr_se_byte(self):
        x = (self.operand & 0x0f00) >> 8
        yy = self.operand & 0x00ff
        if self.v[x] == yy:
            self.pc += 2

    # 4xyy: Skip next instruction if Vx != yy (increment pc by 2)
    def instr_sne(self):
        x = (self.operand & 0x0f00) >> 8
        yy = self.operand & 0x00ff
        if self.v[x] != yy:
            self.pc += 2

    # 5xy0: Skip next instruction if Vx = Vy (increment pc by 2)
    def instr_se_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        if self.v[x] == self.v[y]:
            self.pc += 2
    
    # 6xyy: Vx = yy
    def instr_ld_byte(self):
        x = (self.operand & 0x0f00) >> 8
        self.v[x] = self.operand & 0x00ff

    # 7xyy: Vx += yy
    def instr_add_byte(self):
        x = (self.operand & 0x0f00) >> 8
        self.v[x] += (self.operand & 0x00ff) >> 8
        if self.v[x] > 255: # handle overflow (8-bit).
            self.v[x] -= 256

    # 8xy0: Vx = Vy
    def instr_ld_vx_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] = self.v[y]

    # 8xy1: OR Vx and Vy, store result in Vx
    def instr_or_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] = self.v[x] | self.v[y]

    # 8xy2: AND Vx and Vy, store result in Vy
    def instr_and_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] = self.v[x] & self.v[y]

    # 8xy3: XOR Vx and Vy, store result in Vy
    def instr_xor_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] = self.v[x] ^ self.v[y]

    # 8xy4: Add Vy to Vx. Set Vf = 1 on overflow or Vf = 0 otherwise
    def instr_add_xy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] += self.v[y]
        if self.v[x] > 255: # handle overflow
            self.v[x] -= 256
            self.v[0xf] = 1
        else:
            self.v[0xf] = 0

    # 8xy5: Subtract Vy from Vx and store in Vx. Set Vf = 1 if Vx > Vy or Vf = 0 otherwise
    def instr_sub_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] -= self.v[y]
        if self.v[x] < 0:
            self.v[x] += 256
            self.v[0xf] = 0
        else:
            self.v[0xf] = 1

    # 8xy6: Set Vf = 1 if least-significant bit of Vx is 1 or Vf = 0 otherwise. Then divide Vx by 2. 
    def instr_shr(self):
        x = (self.operand & 0x0f00) >> 8
        if (self.v[x] & 0x000f) % 2 == 0:
            self.v[0xf] = 0
        else:
            self.v[0xf] = 1
        self.v[x] >>= 1

    # 8xy7: Subtract Vx from Vy and store on Vx. Set Vf = 1 if Vx > Vy or Vf = 0 otherwise
    def instr_subn_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        self.v[x] = self.v[y] - self.v[x]
        if self.v[x] < 0:
            self.v[x] += 256
            self.v[0xf] = 0
        else:
            self.v[0xf] = 1

    # 8xyE: Set Vf = 1 if least-significant bit of Vx is 1 or Vf = 0 otherwise. Then multiply Vx by 2. 
    def instr_shr(self):
        x = (self.operand & 0x0f00) >> 8
        if (self.v[x] & 0x000f) % 2 == 0:
            self.v[0xf] = 0
        else:
            self.v[0xf] = 1
        self.v[x] <<= 1

    # 9xy0: Skip next instruction if Vx != Vy (increment pc by 2)
    def instr_sne_vy(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        if self.v[x] != self.v[y]:
            self.pc += 2

    # Axxx: Set register I to xxx
    def instr_ld_i(self):
        self.I = self.operand & 0x0fff

    # Bxxx: Program counter is set to xxx + V0. 
    # Note: Apparently this is not widely used and behaviour is different on SUPER-CHIP 
    def instr_jp_v0(self):
        self.pc = (self.operand & 0x0fff) + self.v[0]

    # Cxyy: Set Vx to a random byte AND yy
    def instr_rnd(self):
        x = (self.operand & 0x0f00) >> 8
        rand = randint(0, 255)
        self.v[x] = rand & (self.operand & 0x00ff)

    # Dxyz: Display z-byte sprite starting from I at (Vx, Vy). Set Vf if a already drawn pixel gets overwritten (XOR).
    def instr_drw(self):
        x = (self.operand & 0x0f00) >> 8
        y = (self.operand & 0x00f0) >> 4
        z = (self.operand & 0x000f)

        x_cord = self.v[x] % 64 # mod screen_width
        y_cord = self.v[y] % 32 # mod screen_height

        self.v[0xf] = 0
        for row in range(z):
            if (y_cord + row) >= 32:
                break
            sprite_row = self.memory[self.I + row] # get sprite
            # split into individual pixels (note: string manipulation might be faster)
            pixels = [
                (sprite_row & 0x80) >> 7,
                (sprite_row & 0x40) >> 6,
                (sprite_row & 0x20) >> 5,
                (sprite_row & 0x10) >> 4,
                (sprite_row & 0x8) >> 3,
                (sprite_row & 0x4) >> 2,
                (sprite_row & 0x2) >> 1,
                (sprite_row & 0x1)
            ]

            for (index, pixel) in enumerate(pixels):
                if pixel == 1:
                    if (x_cord + index) >= 64:
                        break
                    if (self.display.flip_pixel(x_cord + index, y_cord + row)):
                        self.v[0xf] = 1
        self.display.update() # update screen
    
    # Ex9E: Skip next instruction if key with value of Vx is pressed
    def instr_skp(self):
        raise OpcodeNotImplementedException('skip next if key vx is pressed')
    
    # ExA1: Skip next instruction if key with value of Vx is not pressed
    def instr_sknp(self):
        raise OpcodeNotImplementedException('skip next if key vx is not pressed')
    
    # Fx07: Vx = delay timer
    def instr_ld_vx_dt(self):
        x = (self.operand & 0x0f00) >> 8
        self.v[x] = self.timers['delay']

    # Fx0A: Stop execution until key is pressed, then store value of key in Vx
    def instr_ld_vx_k(self):
        raise OpcodeNotImplementedException()
        x = (self.operand & 0x0f00) >> 8
        k = 0xa # @todo: get key here
        self.v[x] = k

    # Fx15: Delay timer = Vx
    def instr_ld_dt_vx(self):
        x = (self.operand & 0x0f00) >> 8
        self.timers['delay'] = self.v[x]

    # Fx18: Sound timer = Vx
    def instr_ld_vx_st(self):
        x = (self.operand & 0x0f00) >> 8
        self.timers['delay'] = self.v[x]

    # Fx1E: I = I + Vx
    def instr_add_i_vx(self):
        x = (self.operand & 0x0f00) >> 8
        self.I += self.v[x] # @todo: overflow?


    # Fx29: I = Location of sprite for digit Vx
    def instr_ld_i_vx(self):
        raise OpcodeNotImplementedException()
    
    # Fx33: Take decimal number in format 'abc' from Vx and store a at I, b at I+1 and c at I+2
    def instr_ld_bcd_vx_i(self):
        x = (self.operand & 0x0f00) >> 8

        a = floor(self.v[x] / 100)
        b = self.v[x] % 100
        b = floor(b / 10)
        c = self.v[x] % 10

        self.memory[self.I] = int(a) # are int checks required?
        self.memory[self.I + 1] = int(b)
        self.memory[self.I + 2] = int(c)

    # Fx55: Put v0 to Vx in memory starting at address in I
    def instr_ld_v0_vx_I(self):
        x = (self.operand & 0x0f00) >> 8
    
        for i in range(x + 1):
            self.memory[self.I + i] = self.v[i]

    # Fx65: Fill v0 to Vx from memory starting at address in I
    def instr_ld_v0_vx_I(self):
        x = (self.operand & 0x0f00) >> 8
    
        for i in range(x + 1):
            self.v[i] = self.memory[self.I + i]
