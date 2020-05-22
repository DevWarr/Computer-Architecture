; expected output:
; #
; ##
; ####
; ########
; ################
; ################################
; ################################################################

; This script has two loops:
; The first loop acts like a for loop,
; starting at 0b00000001 and shifting to the left on each iteration.
; The loop will stop, and the program will HLT once we reach 0b10000000.


    LDI R0,0x01         ; Store our initial value for our for loop
    LDI R1,0x80         ; Store our stopping point for our loop
    LDI R2,0x23         ; Store the value "#" in Register 2
                        ; Leave R3 open for any immediate jumps we need to make
    LDI R4,PrintLoop    ; Store the value of PrintLoop (We jump here a lot)

ForLoop:

    CMP R0,R1           ; Compare R0 to 0x80 (in R1)
    LDI R3,LoopEnd      ; Jump to LoopEnd if we're at the end of our loop
    JEQ R3              

    LDI R1,0            ; Set R1 to zero to prep for our PrintLoop
    JMP R4              ; Jump to PrintLoop

LoopEnd:

    HLT


; PrintLoop is also like a for loop, but actually increments our counter
; instead of left shifting.

PrintLoop:

    CMP R1,R0           ; Compare R1 to our max value of hashes (in R0)
    LDI R3,PrintReturn  ; Jump to PrintReturn if we're at the end of our loop
    JEQ R3

    PRA R2              ; Print a "#"
    INC R1              ; Increment Register 1
    JMP R4              ; Continue the loop (PrintLoop stored at R4)


PrintReturn:

    LDI R3,0x0A         ; Print a new line
    PRA R3
    LDI R3,0x23         ; Reset R3 to the "#" symbol

    LDI R1,0x01         ; shift the bit in R0 by 1
    SHL R0,R1           

    LDI R1,0x80         ; Reset R1 to our 'end value' for the main loop
    LDI R3,ForLoop      ; Load and jump back to the beginning of our main ForLoop
    JMP R3