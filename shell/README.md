# Shell lab

***

### Description

This directory contains the following files:



* pseudoshell.py - a python3 executable file that serves as a basic shell that
  can do the following:

  1. input/ouput redirection

  2. piping, aka "|"

  3. path executable; ex: "/bin/ls"

* p4-output.txt - a txt file used for debugging or running the program for
  input/output redirection. This text file is not necessary for the i/o
  redirectio, but can be used for it.

***

### Running Program

1) You must be using a UNIX OS to assure that this code runs
correctly. Running on Windows may cause issues with the piping code.

2) Make sure to have any version of python3 installed. Python2 is not
supported.

3) Once the above conditions are met, run this command in your terminal or
shell:



	`python3 pseudoshell.py`



4) This command opens up a fake shell which you can input commands such as:



   1. `ls > output.txt` - this writes the output of ls to output.txt

   2. `cat < output.txt` - this uses output.txt as the input for ca
