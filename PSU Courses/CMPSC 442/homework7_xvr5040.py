############################################################
# CMPSC 442: Homework 7
############################################################

student_name = "Xiangyu Ren"


############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    pass


def sudoku_arcs():
    pass


def read_board(path):
    pass


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        pass

    def get_values(self, cell):
        pass

    def remove_inconsistent_values(self, cell1, cell2):
        pass

    def infer_ac3(self):
        pass

    def infer_improved(self):
        pass

    def infer_with_guessing(self):
        pass
