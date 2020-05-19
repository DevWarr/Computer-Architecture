"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0b0] * 0x100
        self.reg = [0] * 0x8
        self.dispatch_table = {
            0x01: self.HLT,
            0x82: self.LDI,
            0x47: self.PRN
        }
        self.ALU_table = {
            0x00: lambda a, b: self.reg[a] + self.reg[b],
            0x01: lambda a, b: self.reg[a] - self.reg[b],
            0x02: lambda a, b: self.reg[a] * self.reg[b],
            0x03: lambda a, b: self.reg[a] // self.reg[b],
            0x04: lambda a, b: self.reg[a] % self.reg[b],
            0x05: lambda a, b: (self.reg[a] + 0x01) & 0xFF,
            0x06: lambda a, b: (self.reg[a] - 0x01) & 0xFF,
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

    def ALU(self, op, reg_a, reg_b):
        """ALU operations."""

        arithmetic = self.ALU_table.get(op)
        if arithmetic is None:
            raise Exception("Unsupported ALU operation")

        if (op == 0x03 or op == 0x04) and self.reg[reg_b] == 0:
            raise Exception("Cannot divide by zero")

        self.reg[reg_a] = arithmetic(reg_a, reg_b)

    def LDI(self, ir):
        self.reg[self.ram_read(self.pc + 1)
                 ] = self.ram_read(self.pc + 2)

    def PRN(self, ir):
        print(self.reg[self.ram_read(self.pc + 1)])

    def HLT(self, ir):
        exit()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
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
        while True:
            self.trace()
            ir = self.ram_read(self.pc)

            if (ir & 0x20) >> 5:
                # ALU
                if ir >> 6 == 0x02:
                    self.ALU(ir & 0x0F, self.ram_read(self.pc + 1),
                             self.ram_read(self.pc+2))
                else:
                    self.ALU(ir & 0x0F, self.ram_read(self.pc + 1), None)
            
            else:
                action = self.dispatch_table.get(ir)
                if action is None:
                    print("Error: Unknown Instruction %02X" % ir)
                    self.trace()
                    exit()
                action(ir)

            if not (ir & 0x10) >> 4:
                # If the program isn't setting the
                # PC for us, we'll do it here
                self.pc += 1 + (ir >> 6)
