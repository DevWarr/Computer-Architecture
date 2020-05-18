# LS-8 Notes

## CPU

### Properties

#### `self.pc`

The Program Counter. This increments every time the program moves, in order to hold onto where the program is currently running.

#### `self.reg`

The registers within the CPU.
R0-R7.

Can hold numbers from `0b00000000` to `0b11111111`

NOTE: Only registers R0-R4 are available. The other registers are used for:

* R5 - Interrupt Mask
* R6 - Interrupt Status
* R7 - Stack Pointer

#### `self.ram`

A storage that holds an address and an instruction.

```py
self.ram = [
    0b10000010,
    0b00000000,
    0b00001000
]
```

Instructions are written in binary, and each byte corresponds to a piece of information or an instruction for the CPU.

In this case, the first instruction tells the CPU that we're going to store information in a register. The second instruction tells the CPU which register we're going to store the information, and the third instruction tells the CPU the value we're going to store.

Some instructions are only one line, while others (like this one) use multiple lines for a full instruction to occur.
