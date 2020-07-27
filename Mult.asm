// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


@i
M = 1 // counter
@2
M = 0 // add sum here
@1
D=M
@LOOP1
D;JLT
@LOOP2
D;JGT
@END
D;JEQ
(LOOP1)
    @i
    D=M
    @1
    D=D+M
    @END
    D;JGT // check end of loop
    @0
    D=M
    @2 // add to sum
    M=M-D
    @i
    M=M+1 // increment counter
    @LOOP1
    0;JMP

(LOOP2)
    @i
    D=M
    @1
    D=D-M
    @END
    D;JGT // check end of loop
    @0
    D=M
    @2 // add to sum
    M=M+D
    @i
    M=M+1 // increment counter
    @LOOP2
    0;JMP
(END)