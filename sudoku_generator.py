import math, random
#from sudoku import *
# Maddy - I commented this so you guys can test that this code works
#if line 2 is not commented, it won't print anything

class SudokuGenerator:
    """
    create a sudoku board - initialize class variables and set up the 2D board
    This should initialize:
    self.row_length		- the length of each row
    self.removed_cells	- the total number of cells to be removed
    self.board			- a 2D list of ints to represent the board
    self.box_length		- the square root of row_length

    Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

    Return:
    None
    """
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.grid = [[0] * 9 for _ in range(9)]  # done by Sabrina for the valid_in_col and _row functions

        self.board = [[0 for row in range(9)] for col in range(9)]
        self.box_length = int((row_length) ** 0.5)

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return [[self.board[row][col] for row in range(9)] for col in range(9)]

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for row in self.board:  # row: ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
            for col in row:  # col: each "-"
                print(col, end=" ")
            print()

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    # Check if num is already present in the specified row
    def valid_in_row(self, row, num):
        return num not in self.grid[row]

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):  # Check if num is already present in the specified column
        for row in range(9):
            if self.grid[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    def unused_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board 
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        if num < 1 or num > 9:
            return False
        for r in range(9):
            if self.board[r][col] == num:
                return False
        for c in range(9):
            if self.board[row][c] == num:
                return False
        if 0 <= row <= 2 and 0 <= col <= 2:
            row_start, col_start = 0, 0
        elif 3 <= row <= 5 and 0 <= col <= 2:
            row_start, col_start = 3, 0
        elif 6 <= row <= 8 and 0 <= col <= 2:
            row_start, col_start = 6, 0
        elif 0 <= row <= 2 and 3 <= col <= 5:
            row_start, col_start = 0, 3
        elif 3 <= row <= 5 and 3 <= col <= 5:
            row_start, col_start = 3, 3
        elif 6 <= row <= 8 and 3 <= col <= 5:
            row_start, col_start = 6, 3
        elif 0 <= row <= 2 and 6 <= col <= 8:
            row_start, col_start = 0, 6
        elif 3 <= row <= 5 and 6 <= col <= 8:
            row_start, col_start = 3, 6
        elif 6 <= row <= 8 and 6 <= col <= 8:
            row_start, col_start = 6, 6
        else:
            row_start, col_start = 10, 10  # this will never happen

        if not self.unused_in_box(row_start, col_start, num):
            return False

        return True

    def generate_random_num(self):
        num = random.randint(1, 9)
        return num

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                num = self.generate_random_num()
                while True:
                    if self.unused_in_box(row_start, col_start, num):
                        self.board[row][col] = num
                        break
                    else:
                        num = self.generate_random_num()

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, 9, 3):  # Loop over the main diagonal starting points
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        total_cells = 81
        cells_to_remove = self.removed_cells
        cells_already_removed = set()
        while len(cells_already_removed) < cells_to_remove:
            row = random.randint(0, len(self.board) - 1)  # Generate random coordinates
            col = random.randint(0, len(self.board[0]) - 1)

            if (row, col) not in cells_already_removed:  # Check if the cell is not already removed
                self.board[row][col] = 0  # Remove the cell by setting its value to 0
                cells_already_removed.add((row, col))  # Add the removed cell to the set


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
