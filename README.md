None-OCR-simple-sudoku-solver-A.I

A simple Python Sudoku solver built with just OpenCV, designed for computers with limited resources. It's well-suited for devices like the Raspberry Pi Zero 2 W or other similar low-resource systems. so simpleit does not require any Machine Learning (ML) techniques such as OCR

How It Works

    Box Detection:
    The program detects a Sudoku puzzle by looking for a box within a specific size range.

    Cell Extraction:
    Once the puzzle is detected, the box is divided into a 9x9 grid using nested loops to isolate each cell.

    Digit Recognition:
    Each cell is compared against .png images (templates) of digits 0-9 stored in a folder called templates.
        The template for "0" is a blank white image.
        If a cell matches a specific template, the program extracts the digit from the file name (dropping the file extension) and assigns that value to the cell.

    Backtracking Solver:
    The recognized digits are stored in memory and used as input for a backtracking algorithm to solve the puzzle.

    Displaying the Solution:
    Finally, the solved Sudoku puzzle is displayed in a window and printed to the terminal.
  
    I have supplied some example puzzles to try out. I will add more in the future by an update of this git!!
    Notice that it only works with type of font but I will find a way  make a modification of the scipts to allow more fonts if I have time.
    
    requirments 
    python3
    opencv for python
    install opencv by pip using this command
    pip3 install opencv-python

    Also please unzip the the templates folder before running Main.py
