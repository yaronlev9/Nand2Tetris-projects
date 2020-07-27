// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Sort.asm

//this file makes a bubble sort on a number of registers given from the higest data to the lowest.
@14
D=M
@start //holds the address of the first data
M=D
@15
D=M
@n1 //number of iterations of main loop
M=D

(MAIN_LOOP)
    @n1
    D=M
    @n2 //initialize number of iterations of inner loop
    M=D-1
    @INNER_LOOP //calls inner loop
    D;JGT
    @END //ends the main loop if n1 reaches 0
    D;JEQ
    (END_LOOP)
    @n1 //decrease n1 by 1
    M=M-1
    @14
    D=M
    @start //initialize start with the address of the first data
    M=D
    @MAIN_LOOP
    D;JGE

(INNER_LOOP)
    @start
    A=M //gets the memory of the first register
    D=M
    @start
    A=M+1 //gets the memory of the second register
    D=D-M
    @SWAP //swaps if first is smaller than the second
    D;JLT
    (END_SWAP)
    @start //start gets the next address
    M=M+1
    @n2 //decrease n2 by 1
    M=M-1
    D=M
    @INNER_LOOP //if n2 is higher than zero continue the iterations
    D;JGT
    @END_LOOP //if n2 is zero or bellow goes back to main loop
    D;JLE

(SWAP)
    //saves the memory of the first address in the temp
    @start
    A=M
    D=M
    @temp
    M=D
    //puts the memory of the second address in the first address
    @start
    A=M+1
    D=M
    @start
    A=M
    M=D
    //puts the memory in the temp to the second address
    @temp
    D=M
    @start
    A=M+1
    M=D
    @END_SWAP
    0;JMP

(END)



