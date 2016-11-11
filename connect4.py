from random import randint
import copy

class Board:
    coords = {}

    def __init__(self):
        self.clear()

    def clear(self):
        for y in range(1, 7):
            for x in range(1, 8):
                self.coords[y, x] = "-"

    def row_isfull(self, position):
        for y in range(1, 7):
            if self.coords[y, position] == "-":
                return False
        return True

    def print(self):
        for y in range(6, 0, -1):
            print(y, end=" ")
            for x in range(1, 8):
                print(self.coords[y, x], end=" ")
            print("")
        print("-", "1", "2", "3", "4", "5", "6", "7")
        print("")

    def possible_moves(self):
        freerowlist = []
        for x in range(1, 8):
            if not self.row_isfull(x):
                freerowlist.append(x)
        return freerowlist

    def make_play(self, position, sign):
        placed = False
        for y in range(1, 7):
            if self.coords[y, position] == "-":
                self.coords[y, position] = sign
                placed = True
                break
        if not placed:
            print("Board is full on column: " + str(position))

    def copy(self):
        newboard = Board()
        newboard.coords = {k: v for k, v in self.coords.items()}
        return newboard


def find_winner(board, player):
    found = False
    for y in range(1, 7):
        for x in range(1, 8):
            if board.coords[y, x] == player:
                if walk_neighbour(board, player, y, x, 1, "right") == 4:
                    print(str(y) + "-" + str(x) + " Winner going right - Player " + player)
                    found = True
                elif walk_neighbour(board, player, y, x, 1, "up") == 4:
                    print(str(y) + "-" + str(x) + " Winner going up - Player " + player)
                    found = True
                elif walk_neighbour(board, player, y, x, 1, "diaup") == 4:
                    print(str(y) + "-" + str(x) + " Winner going diagonal up - Player " + player)
                    found = True
                elif walk_neighbour(board, player, y, x, 1, "diadown") == 4:
                    print(str(y) + "-" + str(x) + " Winner going diagonal down - Player " + player)
                    found = True
                break
    return found


def walk_neighbour(board, player, y, x, connect, direction):
    """
    checks for amount of adjacent 'player' signs for a connect4
    :rtype: int
    :return: amount
    """

    if connect != 4:
        if direction == "right":
            if x < 7:
                if board.coords[y, x + 1] == player:
                    return walk_neighbour(board, player, y, x + 1, connect + 1, "right")

        if direction == "up":
            if y < 6:
                if board.coords[y + 1, x] == player:
                    return walk_neighbour(board, player, y + 1, x, connect + 1, "up")

        if direction == "diaup":
            if x < 7 and y < 6:
                if board.coords[y + 1, x + 1] == player:
                    return walk_neighbour(board, player, y + 1, x + 1, connect + 1, "diaup")

        if direction == "diadown":
            if x < 7 and y > 1:
                if board.coords[y - 1, x + 1] == player:
                    return walk_neighbour(board, player, y - 1, x + 1, connect + 1, "diadown")
    #if connect > 2:
    #    print("Evaluated",x,y,"with score of",connect )
    return connect


def minmax_recursive(board, depth, maxdepth, player):
    points = []
    if depth > maxdepth:
        if player == "X":
            if find_winner(board,"X"):
                return 10
        elif player == "O":
            if find_winner(board,"O"):
                return -10
        return 0
    else:
        for move in board.possible_moves():
            copyboard = copy.deepcopy(board)
            if player == "X":
                copyboard.make_play(move, "X")
                player = "O"
            else:
                copyboard.make_play(move, "O")
                player = "X"
            points.append(minmax_recursive(copyboard, depth + 1, maxdepth, player))
    print(points)
    if points:
        if player == "O":
            return max(points)
        else:
            return min(points)
    return 0
def make_aimove(board, maxdepth):
    movescoredict = {}
    for move in board.possible_moves():
        copyboard = copy.deepcopy(board)
        movescoredict[move] = minmax_recursive(copyboard, 0, maxdepth, "X")
    # Can't do this cuck with nested lists :/
    print(movescoredict)
    x_bestmove = max(movescoredict, key=movescoredict.get)  # <- key from dict
    print(movescoredict)
    print("I would play: ", x_bestmove)
    pass

"""
unable to find winner this cuck, why?
6 - - - - - - -
5 - - - - - - -
4 - O - - - - -
3 - O - - - - -
2 - O - - - - -
1 O O - - - - -
- 1 2 3 4 5 6 7

6 - - - - - - -
5 - - - - - - -
4 - - X - - - -
3 - - X - - - -
2 - - X - - - -
1 X - X - - - -
- 1 2 3 4 5 6 7
"""


b = Board()
b.make_play(2,"X")
b.make_play(2,"X")
b.make_play(2,"X")
b.make_play(3,"O")
b.make_play(4,"O")
b.make_play(7,"O")
b2 = copy.deepcopy(b)
b2.make_play(7,"O")
b2.make_play(7,"O")
b2.make_play(7,"O")
b2.make_play(7,"O")
b2.make_play(7,"O")
b.print()
# Veränderungen in b2 verändern auch b, obwohl copy.deepcuck... ggwp

