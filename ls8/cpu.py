"""CPU functionality."""

import sys
import time


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0b0] * 0x100
        self.reg = [0] * 0x8
        self.reg[7] = 0xF4
        self.fl = 0
        self.dispatch_table = {
            # ALU
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100100: self.MOD,
            0b01100101: self.INC,
            0b01100110: self.DEC,
            0b10100111: self.CMP,
            0b10101000: self.AND,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b10101011: self.XOR,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            # PC Mutators
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b01010111: self.JGT,
            0b01011000: self.JLT,
            0b01011001: self.JLE,
            0b01011010: self.JGE,
            # Other
            0b00000000: self.NOP,
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b10000011: self.LD,
            0b10000100: self.ST,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01000111: self.PRN,
            0b01001000: self.PRA,
        }

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as program:
            for line in program:
                binstr = ""
                for char in line:
                    if char == "\n" or char == "#":
                        break
                    elif char == "0" or char == "1":
                        binstr += char
                if len(binstr) == 8:
                    self.ram_write(address, int(binstr, 2))
                    address += 1

    def ADD(self):
        self.reg[self.ram_read(self.pc+1)
                 ] += self.reg[self.ram_read(self.pc+2)]

    def AND(self):
        self.reg[self.ram_read(self.pc+1)
                 ] &= self.reg[self.ram_read(self.pc+2)]

    def CALL(self):
        self.reg[7] -= 0b01
        mdr = self.pc + 2
        self.ram_write(self.reg[7], mdr)

        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def CMP(self):
        val1 = self.reg[self.ram_read(self.pc+1)]
        val2 = self.reg[self.ram_read(self.pc+2)]
        if val1 == val2:
            self.fl = 0b001
        elif val1 < val2:
            self.fl = 0b100
        else:
            self.fl = 0b010

    def DEC(self):
        self.reg[self.ram_read(self.pc+1)
                 ] = (self.reg[self.ram_read(self.pc+1)
                               ] - 1) & 0b11111111

    def DIV(self):
        if self.reg[self.ram_read(self.pc+2)] == 0:
            raise Exception("Cannot divide by zero")
        self.reg[self.ram_read(self.pc+1)
                 ] //= self.reg[self.ram_read(self.pc+2)]

    def HLT(self):
        exit()

    def INC(self):
        self.reg[self.ram_read(self.pc+1)
                 ] = (self.reg[self.ram_read(self.pc+1)
                               ] + 1) & 0b11111111

    def INT(self):
        pass

    def IRET(self):
        pass

    def JEQ(self):
        if self.fl & 0b001:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def JGE(self):
        if self.fl & 0b011:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def JGT(self):
        if self.fl & 0b010:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def JLE(self):
        if self.fl & 0b101:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def JLT(self):
        if self.fl & 0b100:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def JMP(self):
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def JNE(self):
        if not self.fl & 0b001:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else: 
            self.pc += 2

    def LD(self):
        val_from_mem = self.ram_read(self.reg[self.ram_read(self.pc+2)])
        self.reg[self.ram_read(self.pc+1)
                 ] = val_from_mem

    def LDI(self):
        self.reg[self.ram_read(self.pc + 1)
                 ] = self.ram_read(self.pc + 2)

    def MOD(self):
        if self.reg[self.ram_read(self.pc+2)] == 0:
            raise Exception("Cannot divide by zero")
        self.reg[self.ram_read(self.pc+1)
                 ] %= self.reg[self.ram_read(self.pc+2)]

    def MUL(self):
        self.reg[self.ram_read(self.pc+1)
                 ] *= self.reg[self.ram_read(self.pc+2)]

    def NOP(self):
        pass

    def NOT(self):
        pass

    def OR(self):
        pass

    def POP(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def PRA(self):
        print(chr(self.reg[self.ram_read(self.pc + 1)]))

    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])

    def PUSH(self):
        self.reg[7] -= 0b01
        mdr = self.reg[self.ram_read(self.pc + 1)]
        self.ram_write(self.reg[7], mdr)

    def RET(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def SHL(self):
        self.reg[self.ram_read(self.pc+1)
                 ] <<= self.reg[self.ram_read(self.pc+2)]

    def SHR(self):
        self.reg[self.ram_read(self.pc+1)
                 ] >>= self.reg[self.ram_read(self.pc+2)]

    def ST(self):
        mar = self.reg[self.ram_read(self.pc+1)]
        mdr = self.reg[self.ram_read(self.pc+2)]
        self.ram_write(mar, mdr)

    def SUB(self):
        self.reg[self.ram_read(self.pc+1)
                 ] = (self.reg[self.ram_read(self.pc+1)
                               ] - self.reg[self.ram_read(self.pc+2)]) & 0b11111111

    def XOR(self):
        pass


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        sec_check = time.time()
        while True:

            sec_check_2 = time.time()
            if sec_check_2 - sec_check >= 1:
                sec_check = sec_check_2
                self.reg[6] |= 0b00000001

            # self.trace()
            ir = self.ram_read(self.pc)

            action = self.dispatch_table.get(ir)
            if action is None:
                print(f"Error: Unknown Instruction {bin(ir)}")
                self.trace()
                exit()
            action()

            if not (ir & 0b00010000) >> 4:
                # If the program isn't setting the
                # PC for us, we'll do it here
                self.pc += 1 + (ir >> 6)
