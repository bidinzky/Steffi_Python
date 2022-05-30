import random


###
# TLDR: The  game of life problem gets split into 3 problems
#       1. the Board:
#                    - defines the game Board (like a chess board)
#                    - is able to get to the next state (cells die or get born based on the rules)
#       2. the Cell: implements a simple Cell with some attributes
#                    is_alive defines if there is a living cell (dead and no cell is same)
#                    _age is an example of an attribute each time epoch the cell lives this gets incremented
#                    possible extensions would be e.g. colour, shape, ...
#       3. the Simulator: its job is to initialize the board and move it forward in time if needed and offers a simple CLI interface
###


class Cell:
    def __init__(self, is_alive, age=0):
        self.is_alive = is_alive
        self._age = age

    # method that gets called when the cell lives another round --> age it or set it to 0 if the cell is dead
    def age(self):
        if self.is_alive:
            self._age += 1
        else:
            self._age = 0

    # python method to define how an instance of the Cell class should be printed
    # in this case it should print the age if the cell is alive otherwise it prints a space character
    def __repr__(self):
        return f"{self._age}" if self.is_alive else " "


class Board:
    # Constructor for the Board, size is the number of cells per side so 4 => 4x4 board
    # alive_threshold defines how many percent of the initial cells should be alive
    def __init__(self, size=4, alive_threshold=0.5):
        self.size = size
        self.board = [[Cell(random.random() >= alive_threshold) for _ in range(size)] for _ in range(size)]

    def calculate_next_step(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                alive_neighbours = 0
                for (n_row, n_col) in self.__get_neighbours(row, col):
                    alive_neighbours += self.board[n_row][n_col].is_alive
                if alive_neighbours > 3 or alive_neighbours <= 1:
                    # to many or to little neighbours' cell dies
                    cell.is_alive = False
                elif alive_neighbours == 3:
                    # if cell was dead it now lives, if it lives it still lives
                    cell.is_alive = True
                # with alive_neighbours==2 --> nothing changes
                cell.age()

    def __get_neighbours(self, row, col):
        neighbours = []
        for row_delta in range(-1, 2):  # -1,2 to get range -1 to 1 --> 2 is exclusive
            if 0 <= row + row_delta < self.size:  # if row_delta + row is in the board
                for col_delta in range(-1, 2):
                    if 0 <= col + col_delta < self.size:  # if col + col_delta is in the board
                        if not (col_delta == 0 and row_delta == 0):  # skip self
                            neighbours.append((row + row_delta, col + col_delta))
        return neighbours

    def __repr__(self):
        s = ""
        for row in range(self.size):
            s += str(self.board[row])
            s += "\n"
        return s


class Simulator:
    def __init__(self):
        size = 4
        alive_threshold = 0.7
        try:
            size = int(input("Enter size of the board [4]: "))
        except:
            pass
        try:
            alive_threshold = float(input("Enter threshold of cells to stay alive [.7]: "))
        except:
            pass

        self.board = Board(size, alive_threshold)
        print(self.board)

    def handle(self):
        i = 0
        while True:
            if input("") == "c":  # wait for input, if input is c --> break out of loop
                break
            i += 1
            print(f"epoch {i}")
            self.board.calculate_next_step()
            print(self.board)


s = Simulator()
s.handle()
