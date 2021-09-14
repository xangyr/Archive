############################################################
# CMPSC 442: Homework 3
############################################################


student_name = "Xiangyu Ren"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import queue
import math


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    temp = [*range(1, rows * cols), 0]
    board = [temp[i:i + cols] for i in range(0, rows * cols, cols)]
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.__board = board
        self.__row = len(board)
        self.__col = len(board[0])
        self.__index = self.find_ij()

    def find_ij(self):
        for i in range(self.__row):
            for j in range(self.__col):
                if self.__board[i][j] == 0:
                    return (i, j)

    def get_board(self):
        return self.__board

    def perform_move(self, direction):
        i, j = self.__index
        if direction == 'up':
            if not i:
                return False
            self.__board[i - 1][j], self.__board[i][j] = self.__board[i][j], self.__board[i - 1][j]
            self.__index = (i - 1, j)
            return True
        elif direction == 'down':
            if i == self.__row - 1:
                return False
            self.__board[i + 1][j], self.__board[i][j] = self.__board[i][j], self.__board[i + 1][j]
            self.__index = (i + 1, j)
            return True
        elif direction == 'left':
            if not j:
                return False
            self.__board[i][j - 1], self.__board[i][j] = self.__board[i][j], self.__board[i][j - 1]
            self.__index = (i, j - 1)
            return True
        elif direction == 'right':
            if j == self.__col - 1:
                return False
            self.__board[i][j + 1], self.__board[i][j] = self.__board[i][j], self.__board[i][j + 1]
            self.__index = (i, j + 1)
            return True
        else:
            return False

    def scramble(self, num_moves):
        directions = ['up', 'down', 'left', 'right']
        for i in range(num_moves):
            self.perform_move(random.choice(directions))

    def is_solved(self):
        temp = [*range(1, self.__row * self.__col), 0]
        board = [temp[i:i + self.__col] for i in range(0, self.__row * self.__col, self.__col)]
        return self.__board == board

    def copy(self):
        return TilePuzzle([[j for j in i] for i in self.__board])

    def successors(self):
        directions = ['up', 'down', 'left', 'right']
        for i in directions:
            temp = self.copy()
            if temp.perform_move(i):
                yield (i, temp)

    def iddfs_helper(self, limit, moves):
        if limit == 0:
            yield None
        else:
            for next_move, next_board in self.successors():
                if next_board.is_solved():
                    yield moves + [next_move]
                for path in next_board.iddfs_helper(limit - 1, moves + [next_move]):
                    yield path

    # Required
    def find_solutions_iddfs(self):
        limit = 0
        flag = False

        if self.is_solved():
            yield []

        while not flag:
            for soln in self.iddfs_helper(limit, []):
                if soln:
                    flag = True
                    yield soln
            limit += 1

    def man_dis_h(self):
        h = 0
        for i in range(self.__row):
            for j in range(self.__col):
                if self.__board[i][j] == 0:
                    h += abs(self.__row - 1 - i) + abs(self.__col - 1 - j)
                    continue
                h += abs((self.__board[i][j] - 1) % self.__col - j) + abs(
                    (self.__board[i][j] - 1) // self.__col - i)
        return h

    # Required
    def find_solution_a_star(self):
        visited = set()
        path = []
        f, g = self.man_dis_h(), 0
        frontier = queue.PriorityQueue()
        board = self.copy()
        frontier.put([f, g, path, board])

        while not frontier.empty():
            f, g, path, board = frontier.get()
            if board in visited:
                continue
            visited.add(tuple(tuple(i) for i in board.get_board()))

            if board.is_solved():
                return path
            for next_move, next_board in board.successors():
                next_board_t = tuple(tuple(i) for i in next_board.get_board())
                if next_board_t not in visited:
                    frontier.put([next_board.man_dis_h() + g, g + 1, path + [next_move], next_board])
        return None


############################################################
# Section 2: Grid Navigation
############################################################
def grid_successor(current, scene):
    valid = ['up left', 'up', 'up right', 'left', 'right', 'down left', 'down', 'down right']
    x, y = current
    move_list = []
    for move in valid:
        new_x, new_y = x, y
        if 'up' in move:
            new_x = x - 1
        if 'down' in move:
            new_x = x + 1
        if 'left' in move:
            new_y = y - 1
        if 'right' in move:
            new_y = y + 1
        if 0 <= new_x < len(scene) and 0 <= new_y < len(scene[0]):
            move_list.append((new_x, new_y))
    for x, y in move_list:
        if not scene[x][y]:
            yield x, y


def euc_dis_h(current, goal):
    return math.sqrt(math.pow(goal[0] - current[0], 2) + math.pow(goal[1] - current[1], 2))


def find_path(start, goal, scene):
    visited = set()
    path = []
    f, g = euc_dis_h(start, goal), 0
    frontier = queue.PriorityQueue()
    frontier.put([f, g, path, start])

    while not frontier.empty():
        f, g, path, pos = frontier.get()
        if pos in visited:
            continue
        visited.add(pos)

        if pos == goal:
            return [start] + path
        for next in grid_successor(pos, scene):
            if next not in visited:
                frontier.put([euc_dis_h(next, goal) + g, g + 1, path + [next], next])
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
def distinct_successor(length, board):
    for i in range(length):
        if board[i]:
            if i - 2 >= 0 and board[i - 1] and not board[i - 2]:
                temp = board[:]
                temp[i - 2], temp[i] = temp[i], temp[i - 2]
                yield (i, i - 2), temp
            if i - 1 >= 0 and not board[i - 1]:
                temp = board[:]
                temp[i - 1], temp[i] = temp[i], temp[i - 1]
                yield (i, i - 1), temp
            if i + 1 < length and not board[i + 1]:
                temp = board[:]
                temp[i + 1], temp[i] = temp[i], temp[i + 1]
                yield (i, i + 1), temp
            if i + 2 < length and board[i + 1] and not board[i + 2]:
                temp = board[:]
                temp[i + 2], temp[i] = temp[i], temp[i + 2]
                yield (i, i + 2), temp


def distinct_h(current, goal):
    h = 0
    for i in range(len(goal)):
        if current[i]:
            h += abs(goal.index(current[i]) - i)
    return h


def solve_distinct_disks(length, n):
    if length == 0:
        return []
    elif length <= n:
        return None

    start = [i + 1 if i < n else None for i in range(length)]
    goal = [None if i < length - n else length - i for i in range(length)]

    visited = set()
    path = []
    f, g = distinct_h(start, goal), 0
    frontier = queue.PriorityQueue()
    frontier.put([f, g, path, start])

    while not frontier.empty():
        f, g, path, current = frontier.get()
        if tuple(current) in visited:
            continue
        visited.add(tuple(current))

        if current == goal:
            return path
        for next_move, next_board in distinct_successor(length, current):
            if tuple(next_board) not in visited:
                frontier.put([distinct_h(next_board, goal) + g, g + 1, path + [next_move], next_board])
    return None


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = [[False for j in range(cols)] for i in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.__board = board
        self.__row = len(board)
        self.__col = len(board[0])

    def get_board(self):
        return self.__board

    def reset(self):
        self.__board = [[False for j in range(self.__col)] for i in range(self.__row)]

    def is_legal_move(self, rows, cols, vertical):
        if vertical:
            if 0 <= rows < self.__row - 1 and 0 <= cols <= self.__col - 1:
                return not self.__board[rows + 1][cols] and not self.__board[rows][cols]
            else:
                return False
        else:
            if 0 <= rows <= self.__row - 1 and 0 <= cols < self.__col - 1:
                return not self.__board[rows][cols] and not self.__board[rows][cols + 1]
            else:
                return False

    def legal_moves(self, vertical):
        for i in range(self.__row):
            for j in range(self.__col):
                if self.is_legal_move(i, j, vertical):
                    yield i, j

    def perform_move(self, rows, cols, vertical):
        if vertical:
            self.__board[rows][cols], self.__board[rows + 1][cols] = True, True
        else:
            self.__board[rows][cols], self.__board[rows][cols + 1] = True, True

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical))
        return False if moves else True

    def copy(self):
        return DominoesGame([[self.__board[i][j] for j in range(self.__col)] for i in range(self.__row)])

    def successors(self, vertical):
        for i in range(self.__row):
            for j in range(self.__col):
                if self.is_legal_move(i, j, vertical):
                    temp = self.copy()
                    temp.perform_move(i, j, vertical)
                    yield (i, j), temp

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))

    # Required
    def get_best_move(self, vertical, limit):
        pass
