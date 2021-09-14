############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Xiangyu Ren"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return math.factorial(n * n) / (math.factorial(n) * math.factorial(n * n - n))


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    size = len(board)
    Flag = False if size != len(set(board)) else True
    Flag = Flag and all([j - i != abs(board[i] - board[j]) for i in range(size) for j in range(i + 1, size)])
    return Flag


def n_queens_solutions(n, board=[]):
    if len(board) == n:
        yield board
    children = [board + [i] for i in range(n) if n_queens_valid(board + [i])]
    for child in children:
        yield from n_queens_solutions(n, child)


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.__board = board
        self.__row = len(board)
        self.__col = len(board[0])

    def get_board(self):
        return self.__board

    def perform_move(self, row, col):
        self.__board[row][col] = not self.__board[row][col]
        if row:
            self.__board[row - 1][col] = not self.__board[row - 1][col]
        if self.__row - 1 - row:
            self.__board[row + 1][col] = not self.__board[row + 1][col]
        if col:
            self.__board[row][col - 1] = not self.__board[row][col - 1]
        if self.__col - 1 - col:
            self.__board[row][col + 1] = not self.__board[row][col + 1]

    def scramble(self):
        for i in range(self.__row):
            for j in range(self.__col):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        return not any([any(i) for i in self.__board])

    def copy(self):
        return LightsOutPuzzle([i[:] for i in self.__board])

    def successors(self):
        for i in range(self.__row):
            for j in range(self.__col):
                temp = self.copy()
                temp.perform_move(i, j)
                yield (i, j), temp

    def find_solution(self):
        if self.is_solved():
            return
        temp = self.copy()
        queue = [temp]
        visited = []
        path = {temp: tuple()}
        while queue:
            node = queue.pop(0)
            if node.is_solved():
                print(len(path[node]))
                return list(path[node])
            if node.get_board() in visited:
                continue
            visited.append(node.get_board())
            for move, new_n in node.successors():
                queue.append(new_n)
                path[new_n] = tuple([move]) if not path[node] else tuple([*path[node], move])
                print(path[new_n])
        return None


def create_puzzle(rows, cols):
    puzzle = [[False] * cols] * rows
    return LightsOutPuzzle(puzzle)


############################################################
# Section 3: Linear Disk Movement
############################################################
class LinearDiskMv(object):
    def __init__(self, length, n, flag=False, cell=[]):
        self.__length = length
        self.__n = n
        self.__flag = flag  # T for distinct, F for identical
        if not cell:
            self.__cells = [i + 1 if i < n else None for i in range(length)] if flag else [1 if i < n else None for i in
                                                                                           range(length)]
        else:
            self.__cells = cell

    def get_cell(self):
        return self.__cells

    def perform_move(self, ori, new):
        self.__cells[new], self.__cells[ori] = self.__cells[ori], self.__cells[new]

    def is_solved(self):
        return self.__cells[-self.__n:] == list(range(self.__n, 0, -1)) if self.__flag else all(
            self.__cells[-self.__n:])

    def copy(self):
        return LinearDiskMv(self.__length, self.__n, self.__flag, self.__cells[:])

    def successors(self):
        new_j = 0
        for i, cell in enumerate(self.__cells):
            if cell:
                x, y = -2, 3
                if i == 1: x = -1
                if i == 0: x = 0
                if self.__length - i == 2: y = 2
                if self.__length - i == 1: y = 1
                cells = [None] * (i + x) + self.__cells[i + x: i + y] + [None] * (self.__length - y - i)
                movelist = [z for z in range(len(cells)) if not cells[z]]
                for j in movelist:
                    if i > 2: new_j = j + i - 2
                    if abs(j - i) == 1 or (j - i == 2 and cells[i + 1]) or (i - j == 2 and cells[i - 1]):
                        temp = self.copy()
                        temp.perform_move(i, j)
                        yield (i, j), temp

    def search(self):
        temp = self.copy()
        queue = [temp]
        visited = []
        path = {temp: tuple()}
        while queue:
            node = queue.pop(0)
            if node.is_solved():
                return list(path[node])
            if node.get_cell() in visited:
                continue
            visited.append(node.get_cell())
            for move, new_n in node.successors():
                queue.append(new_n)
                path[new_n] = tuple([move]) if not path[node] else tuple([*path[node], move])
        return None


def solve_identical_disks(length, n):
    return LinearDiskMv(length, n, False).search()


def solve_distinct_disks(length, n):
    return LinearDiskMv(length, n, True).search()
