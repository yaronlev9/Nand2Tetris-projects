// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


//the main loop that checks if a button is pressed
(MAIN_LOOP)
	@SCREEN
	D=A
	@ADDRESS
	M=D
	@KBD
	D=M
	@BLACK_LOOP
	D;JNE
	@WHITE_LOOP
	0;JEQ

//the loop that goes over all screen cells and makes then black
(BLACK_LOOP)
	@ADDRESS
	A=M
	D=M
	@MAIN_LOOP
    D;JNE //checks if the screen cell is black if yes it goes back to the main loop
	@24575
	D=D-A
	@END //ends loop if finished all screen cells
	D;JGT
	@ADDRESS
	A=M
	M=-1 //makes the cell white
	@ADDRESS
	M=M+1
	@BLACK_LOOP
	0;JMP

//the loop that goes over all screen cells and makes then white
(WHITE_LOOP)
    @ADDRESS
    A=M
    D=M
    @MAIN_LOOP
    D;JEQ //checks if the screen cell is white if yes it goes back to the main loop
	@24575
	D=D-A
	@END //ends loop if finished all screen cells
	D;JGT
	@ADDRESS
	A=M
	M=0 //makes the cell white
	@ADDRESS
	M=M+1
	@WHITE_LOOP
	0;JMP

//when exits the loops goes back to main loop
(END)
	@MAIN_LOOP
	0;JMP




