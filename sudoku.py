# main python file where main function will be run
# This file will contain code to create the different screens
# of the project (game start, game over, and game in
# progress), and will form a cohesive project together with
# the rest of the code

import pygame, sys
from sudoku_generator import *

cell_value_list = [
            ['-' for j in range(9)]
            for i in range(9)]

class Cell:
    #represents a single cell (there are 81 total cells)

    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = None

    def set_cell_value(self, value): # cell's value
        self.value = value

    def set_sketched_value(self, value): # cell's sketched value
        self.sketched_value = value

    '''
    Draws this cell, along with the value inside it.
    If this cell has a nonzero value, that value is displayed.
    Otherwise, no value is displayed in the cell.
    The cell is outlined red if it is currently selected.
    '''
    def draw(self):
        #make a variable to keep track of whether it is sketched or real


        real_value_font = pygame.font.Font(None, 40)
        real_value_surf = real_value_font.render(f'{self.value}', True, 'black')

        sketched_value_font = pygame.font.Font(None, 40)
        sketched_value_surf = sketched_value_font.render(f'{self.sketched_value}', True, 'azure4')

        if self.value != 0:
            #draw cell's absolute values on screen in middle
            real_value_rect = real_value_surf.get_rect(center=(self.col * 68 + 68/2, self.row * 68 + 68/2))
            self.screen.blit(real_value_surf, real_value_rect)

        if self.sketched_value != None:
            #draw sketched cell's value on top left corner of cell
            sketched_value_rect = sketched_value_surf.get_rect(center=(self.col * 68 + 15, self.row * 68 + 20))
            self.screen.blit(sketched_value_surf, sketched_value_rect)

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        # this list is the 9x9 2d list that contains the original sudoku board
        self.board = generate_sudoku(9, difficulty)

        #this list contains 81 cell objects
        self.cells = [
            [Cell(self.board[i][j], i, j, screen) for j in range(9)]
            for i in range(9)
        ]

    ''' for def draw(self)
    Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
    Draws every cell on this board.
    '''
    def draw(self):
        # draw thick horizontal lines
        for i in range(1, 4):
            pygame.draw.line(
                self.screen,
                'black',
                (0, i * 204),
                (612, i * 204),
                7
            )
        # draw thick vertical lines
        for i in range(1, 3):
            pygame.draw.line(
                self.screen,
                'black',
                (i * 204, 0),
                (i * 204, 612),
                7
            )

        # draw thin horizontal lines
        for i in range(1, 10):
            pygame.draw.line(
                self.screen,
                'black',
                (0, i * 68),
                (612, i * 68),
                3
            )
        # draw thin vertical lines
        for i in range(1, 10):
            pygame.draw.line(
                self.screen,
                'black',
                (i * 68, 0),
                (i * 68, 612),
                3
            )

    ''' for def select(self, row, col)
    Marks the cell at (row, col) in the board as the current selected cell.
    Once a cell has been selected, the user can edit its value or sketched value.
    '''
    def select(self, row, col):
        #upper line
        pygame.draw.line(
            self.screen,
            'red',
            (col * 68, row * 68),
            ((col+1) * 68, row * 68),
            3
        )

        #bottom line
        pygame.draw.line(
            self.screen,
            'red',
            (col * 68, (row+1) * 68),
            ((col+1) * 68, (row+1) * 68),
            3
        )

        #left line
        pygame.draw.line(
            self.screen,
            'red',
            (col * 68, row * 68),
            (col * 68, (row+1) * 68),
            3
        )

        #right line
        pygame.draw.line(
            self.screen,
            'red',
            ((col+1) * 68, row * 68),
            ((col+1) * 68, (row+1) * 68),
            3
        )

    ''' for def click(self, x, y)
    If a tuple of (x, y) coordinates is within the displayed board, this function returns a tuple of the (row, col)
    of the cell which was clicked. Otherwise, this function returns None.
    '''

    def click(self, x, y):
        if 0 <= x <= 612 and 0 <= y <= 612:
            row = y // 68
            col = x // 68
            position = (row, col)
            return position
        else:
            return None

    ''' for clear(self)
    Clears the value cell. Note that the user can only remove the cell values and sketched value that are
    filled by themselves.
    '''
    def clear(self, row, col):
        if self.board[row][col] == 0:
            # Fill the cell with the background color
            cell_rect = pygame.Rect(col * 69, row * 69, 50, 55)
            pygame.draw.rect(self.screen, 'pink', cell_rect)

            self.cells[row][col].value = 0  # i don't know if the sketched affects the value or not, so just in case
            self.cells[row][col].sketched_value = None
            self.cells[row][col].draw()

    ''' for sketch(self, value)
    Sets the sketched value of the current selected cell equal to user entered value.
    It will be displayed at the top left corner of the cell using the draw() function.
    '''
    def sketch(self, value, row, col):
        self.cells[row][col].sketched_value = value

    ''' for place_number(self, value)
    Sets the value of the current selected cell equal to user entered value.
    Called when the user presses the Enter key.
    '''
    def place_number(self, value, row, col):
        # self.cells[row][col].value = value
        # Convert the value to an integer before assigning
        self.cells[row][col].value = int(value)

    ''' for reset_to_original(self)
    Reset all cells in the board to their original values 
    (0 if cleared, otherwise the corresponding digit).
    '''
    def reset_to_original(self):
        # Reset user-modified cell values and sketched values
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:  # Check if the cell is user-modified
                    self.cells[i][j].value = 0
                    self.cells[i][j].sketched_value = None

    ''' for is_full(self)
    Returns a Boolean value indicating whether the board is full or not.
    '''

    def is_full(self):
        for i in self.cells:
            for j in i:
                if j.value == 0:
                    return False
        return True

    ''' for update_board(self)
    Updates the underlying 2D board with the values in all cells.
    '''

    def update_board(self):
        return [
            [Cell(self.cells[i][j], i, j, self.screen) for j in range(9)]
            for i in range(9)
        ]

    ''' for find_empty(self)
    Finds an empty cell and returns its row and col as a tuple (x, y).
    '''

    def find_empty(self):
        pass

    ''' for check_board(self)
    Check whether the Sudoku board is solved correctly.
    '''

    #def check_board(self):
        # for i in range(9):
        #     for j in range(9):
        #         cell_value_list[i][j] = self.cells[i][j].value
        #
        # for row in range(9):
        #     for col in range(9):
        #         if not board_is_valid(row, col, cell_value_list[row][col]):
        #             return False
        # return True

    def check_board(self):
        # Check rows
        for row in range(9):
            if not self.is_valid_row(row): # if this is not true
                return False # return this function as false

        # Check columns
        for col in range(9):
            if not self.is_valid_col(col): # if this is not true
                return False # return this function as false

        # Check 3x3 boxes
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.is_valid_box(row, col): # if this is not true
                    return False # return this function as false

        return True

    def is_valid_row(self, row):
        seen = set() # This set will be used to keep track of the values seen in the row to ensure no duplicates.
        for col in range(9): # loops through each col index in the range from 0 to 8
            value = self.cells[row][col].value # Gets the cell value
            if value in seen: return False # if it is seen, it finds that the sudoku rule wasn't met
            seen.add(value) # adds the number to the list (basically updates it)
        return True # complete and no duplicates??????? returns True!!! WHOOP WHOOP

    def is_valid_col(self, col):
        seen = set()
        for row in range(9):
            value = self.cells[row][col].value
            if value in seen: return False
            seen.add(value)
        return True

    def is_valid_box(self, row, col):
        seen = set()
        for i in range(3):
            for j in range(3):
                value = self.cells[row + i][col + j].value # row/col change the box and i/j change cell
                if value in seen:
                    return False
                seen.add(value)
        return True


def difficulty_button(x_size, y_size, x_coord, y_coord, text, screen):
    button_surf = pygame.Surface((x_size, y_size))
    button_surf.fill('magenta3')
    button_rect = button_surf.get_rect(topleft = (x_coord, y_coord))
    button_text = pygame.font.Font(None, 30)
    button_text_surf = button_text.render(text, True, 'lightpink1')
    button_text_rect = button_text_surf.get_rect(center = button_rect.center)
    screen.blit(button_surf, button_rect)
    screen.blit(button_text_surf, button_text_rect)

def in_game_button(x_size, y_size, x_coord, y_coord, text, screen):
    in_game_button_surf = pygame.Surface((x_size, y_size))
    in_game_button_surf.fill('darkgoldenrod1')
    button_rect = in_game_button_surf.get_rect(topleft = (x_coord, y_coord))
    button_text = pygame.font.Font(None, 30)
    button_text_surf = button_text.render(text, True, 'white')
    button_text_rect = button_text_surf.get_rect(center = button_rect.center)
    screen.blit(in_game_button_surf, button_rect)
    screen.blit(button_text_surf, button_text_rect)

def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")
    screen = pygame.display.set_mode((612, 680))
    game_start_screen = True
    game_won_screen = False
    game_over_screen = False
    my_board = None
    in_game_button_used = False

    var = 0  # This variable checks that the user selects a cell before a sketched value can be added
    value = 0
    row, col = 0, 0  # > for arrow keys

    while True:

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user exists out of the window
                pygame.quit()
                sys.exit()

            if game_start_screen:  # welcome screen
                game_start_image = pygame.image.load("start_frenchie.png")
                screen.blit(game_start_image, (0, 0))

                # welcome text
                welcome_font = pygame.font.Font(None, 70)
                welcome_surf = welcome_font.render("Welcome to Sudoku", True, 'magenta3')
                welcome_rect = welcome_surf.get_rect(center=(306, 150))
                screen.blit(welcome_surf, welcome_rect)

                # buttons
                difficulty_button(80, 40, 120, 455, "Easy", screen)  # easy
                difficulty_button(100, 40, 260, 455, "Medium", screen)  # medium
                difficulty_button(80, 40, 420, 455, "Hard", screen)  # hard

                # checking for if any buttons clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 120 <= x <= 200 and 455 <= y <= 495:  # easy >> Generate Sudoku board with difficulty 30
                        difficulty_level = 30

                    elif 260 <= x <= 340 and 455 <= y <= 495:  # medium >> Generate Sudoku board with difficulty 40
                        difficulty_level = 40

                    elif 420 <= x <= 500 and 455 <= y <= 495:  # hard >> Generate Sudoku board with difficulty 50
                        difficulty_level = 50
                    elif 0 <= x <= 100 and 0 <= y <= 100: # just to make checking easier
                        difficulty_level = 1 # delete both of these lines later

                    else:
                        continue

                    my_board = Board(612, 680, screen, difficulty_level)
                    screen.fill('pink')  # background turns pink
                    my_board.draw()  # board gets drawn in
                    # this actually draws the characters on the screen
                    for i in range(9):
                        for j in range(9):
                            my_board.cells[i][j].draw()
                    in_game_button(80, 40, 120, 630, "RESET", screen)  # reset
                    in_game_button(100, 40, 260, 630, "RESTART", screen)  # restart
                    in_game_button(80, 40, 420, 630, "EXIT", screen)  # exit
                    game_start_screen = False  # bye-bye frenchie



            # Sabrina >> we can delete/modify later >> what I was working on
            elif event.type == pygame.MOUSEBUTTONDOWN:  # if the user clicks on the board
                var = 1 #variable making sure that a cell was selected before the user can type in a value
                x, y = pygame.mouse.get_pos()  # Get the mouse position
                #clicked_position = my_board.click(x, y)  # mouse position >> board position
                if my_board is not None and y <= 612:
                    row, col = my_board.click(x, y)
                    my_board.draw()
                    my_board.select(row, col)
                if y > 612:
                    in_game_button_used = True

            if event.type == pygame.KEYDOWN and var != 0:  # var checks that a cell has been selected before putting in a sketched value
                value = my_board.cells[row][col].sketched_value
                if my_board.board[row][col] == 0:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        my_board.clear(row, col)
                        my_board.sketch("1", row, col)

                    elif event.key == pygame.K_BACKSPACE:
                        my_board.clear(row, col)
                    # checks for the row of numbers and the keypad numbers

                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        my_board.clear(row, col)
                        my_board.sketch("2", row, col)

                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        my_board.clear(row, col)
                        my_board.sketch("3", row, col)

                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        my_board.clear(row, col)
                        my_board.sketch("4", row, col)


                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        my_board.clear(row, col)
                        my_board.sketch("5", row, col)

                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        my_board.clear(row, col)
                        my_board.sketch("6", row, col)

                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        my_board.clear(row, col)
                        my_board.sketch("7", row, col)

                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        my_board.clear(row, col)
                        my_board.sketch("8", row, col)

                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        my_board.clear(row, col)
                        my_board.sketch("9", row, col)

                    my_board.cells[row][col].draw()  # layers the number and the pink bg color on top of the old one
                    my_board.select(row, col)  # this is here because we want the selection box to still show

                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if value != None:
                            if my_board.cells[row][col].sketched_value != None:
                                my_board.clear(row, col)
                                my_board.place_number(str(value), row, col)
                                my_board.cells[row][col].draw()

            if event.type == pygame.KEYDOWN:  # if a key is pressed
                # my_board.draw() >> can't put here because it'll clear the box for any key pressed
                if event.key == pygame.K_UP:
                    # Move the selection box up
                    var = 1
                    if row > 0:
                        row -= 1
                    my_board.draw()
                    my_board.select(row, col)
                elif event.key == pygame.K_DOWN:
                    # Move the selection box down
                    var = 1
                    if row < 8:
                        row += 1
                    my_board.draw()
                    my_board.select(row, col)
                elif event.key == pygame.K_LEFT:
                    # Move the selection box left
                    var = 1
                    if col > 0:
                        col -= 1
                    my_board.draw()
                    my_board.select(row, col)
                elif event.key == pygame.K_RIGHT:
                    # Move the selection box right
                    var = 1
                    if col < 8:
                        col += 1
                    my_board.draw()
                    my_board.select(row, col)

            if event.type == pygame.MOUSEBUTTONDOWN and in_game_button_used:
                x, y = pygame.mouse.get_pos()
                # If the user selects the RESET button
                if 120 <= x <= 200 and 630 <= y <= 670:
                    my_board.reset_to_original()
                    screen.fill('pink')
                    my_board.draw()
                    for i in range(9):
                        for j in range(9):
                            my_board.cells[i][j].draw()
                    in_game_button(80, 40, 120, 630, "RESET", screen)  # reset
                    in_game_button(100, 40, 260, 630, "RESTART", screen)  # restart
                    in_game_button(80, 40, 420, 630, "EXIT", screen)  # exit

                # If the user selects the RESTART button
                if 260 <= x <= 360 and 630 <= y <= 670:
                    game_start_screen = True
                    screen.fill('pink')  # Clear the screen
                    my_board = None  # Reset the board object

                # If the user selects the EXIT button
                if 420 <= x <= 500 and 630 <= y <= 670:
                    pygame.quit()
                    sys.exit()

            if my_board is not None:
                if my_board.is_full():

                    if my_board.check_board() is True:
                        game_won_screen = True

                    elif my_board.check_board() is False:
                        game_over_screen = True

            if game_won_screen:
                pygame.time.delay(500)
                game_won = pygame.image.load("happy_frenchie.png")
                screen.blit(game_won, (0, 0))
                game_over_font = pygame.font.Font(None, 80)
                game_won_surf = game_over_font.render("Game Won!", 0, 'magenta3')
                game_won_rect = game_won_surf.get_rect(center=(306, 200))
                screen.blit(game_won_surf, game_won_rect)

                difficulty_button(80, 40, 420, 630, "EXIT", screen)  # exit
                x, y = pygame.mouse.get_pos()
                # If the user selects the EXIT button
                if 420 <= x <= 500 and 630 <= y <= 670:
                    pygame.quit()
                    sys.exit()


            if game_over_screen:
                pygame.time.delay(500)
                game_over = pygame.image.load("side_eye_frenchie.png")
                screen.blit(game_over, (0, 0))
                game_over_font = pygame.font.Font(None, 80)
                game_over_surf = game_over_font.render("Game Over...", 0, 'magenta3')
                game_over_rect = game_over_surf.get_rect(center=(200, 100))
                screen.blit(game_over_surf, game_over_rect)

                difficulty_button(100, 40, 260, 630, "RESTART", screen)  # restart
                x, y = pygame.mouse.get_pos()
                if 260 <= x <= 360 and 630 <= y <= 670:
                    game_over_screen = False
                    game_won_screen = False
                    game_start_screen = True
                    my_board = None


            pygame.display.update()


if __name__ == '__main__':
    main()