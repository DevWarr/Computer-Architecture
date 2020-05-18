"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0b0] * 0x100
        self.reg = [0] * 0x8

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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                raise Exception("Cannot divide by zero")
            else:
                self.reg[reg_a] //= self.reg[reg_b]
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                raise Exception("Cannot divide by zero")
            else:
                self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
            # self.trace()
            ir = self.ram_read(self.pc)

            if ir == 0x01:  # HLT
                exit()

            if ir == 0x82:  # LDI
                self.reg[self.ram_read(self.pc + 1)
                         ] = self.ram_read(self.pc + 2)
                self.pc += 1 + 2

            elif ir == 0x47:  # PRN
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 1 + 1

            elif ir == 0xA0:
                self.alu("ADD", self.ram_read(self.pc + 1),
                         self.ram_read(self.pc+2))
                self.pc += 1 + 2
            elif ir == 0xA1:
                self.alu("SUB", self.ram_read(self.pc + 1),
                         self.ram_read(self.pc+2))
                self.pc += 1 + 2
            elif ir == 0xA2:
                self.alu("MUL", self.ram_read(self.pc + 1),
                         self.ram_read(self.pc+2))
                self.pc += 1 + 2
            elif ir == 0xA3:
                self.alu("DIV", self.ram_read(self.pc + 1),
                         self.ram_read(self.pc+2))
                self.pc += 1 + 2
            elif ir == 0xA4:
                self.alu("MOD", self.ram_read(self.pc + 1),
                         self.ram_read(self.pc+2))
                self.pc += 1 + 2

            else:
                print("Error: Unknown Instruction %02X" % ir)
                self.trace()
                exit()
