// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Divide.asm

//this file gets 2 number and divides them and puts the result in R15
@13
D=M
@a //first number that is divided
M=D
@14
D=M
@b //the divisor
M=D
@result
M=0
@a
D=M
@b
D=D-M //checks if the number divided is lower than the divisor
@END
D;JLT
@a
D=M
@result
M=D
@b
D=M-1
@END //check if divisor is 1 than returns a
D;JEQ
@counter
M=1 //sets counter
@result
M=0 //sets result
@LOOP1
0;JMP

(LOOP1)
    @b
    D=M<<
    @a
    D=D-M //checks if number is higher than the number that is divided
    @LOOP2
    D;JGT
    @b
    M=M<< //multiplies divisor by 2
    @counter
    M=M<< //multiplies counter by 2
    @LOOP1
    0;JMP

(LOOP2)
    @counter
    D=M
    @END
    D;JLE //checks if counter is bellow 0
    @b
    D=M
    @a
    D=M-D
    @ADD_RESULT
    D;JGE
    @DECREASE_COUNTER
    0;JMP

(ADD_RESULT)
    // adds the counter to the result and reduces b from a
    @b
    D=M
    @a
    M=M-D
    @counter
    D=M
    @result
    M=M+D
    @DECREASE_COUNTER
    0;JMP

(DECREASE_COUNTER)
    //decreases the counter and b by 2
    @counter
    M=M>>
    @b
    M=M>>
    @LOOP2
    0;JMP

(END)
    //puts the data in result in register R15
    @result
    D=M
    @15
    M=D



