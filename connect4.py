import random, time

class Board:
    def __init__(self):
        self.coords = {}
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
                # if not placed:
                #    print("Board is full on column: " + str(position))

    def copy(self):
        newboard = Board()
        newboard.coords = {k: v for k, v in self.coords.items()}
        return newboard


def find_winner(board):
    for y in range(1, 7):
        for x in range(1, 8):
            if board.coords[y, x] != "-":
                player = board.coords[y, x]
                if walk_neighbour(board, player, y, x, 1, "right") == 4:
                    # print(str(y) + "-" + str(x) + " Winner going right - Player " + player)
                    return player
                elif walk_neighbour(board, player, y, x, 1, "up") == 4:
                    # print(str(y) + "-" + str(x) + " Winner going up - Player " + player)
                    return player
                elif walk_neighbour(board, player, y, x, 1, "diaup") == 4:
                    # print(str(y) + "-" + str(x) + " Winner going diagonal up - Player " + player)
                    return player
                elif walk_neighbour(board, player, y, x, 1, "diadown") == 4:
                    # print(str(y) + "-" + str(x) + " Winner going diagonal down - Player " + player)
                    return player
    return None


def walk_neighbour(board, player, y, x, connect, direction):
    if connect != 4:
        if direction == "right":
            if x < 7:
                if board.coords[y, x + 1] == player:
                    return walk_neighbour(board, player, y, x + 1, connect + 1, "right")
            return connect

        if direction == "up":
            if y < 6:
                if board.coords[y + 1, x] == player:
                    return walk_neighbour(board, player, y + 1, x, connect + 1, "up")
            return connect

        if direction == "diaup":
            if x < 7 and y < 6:
                if board.coords[y + 1, x + 1] == player:
                    return walk_neighbour(board, player, y + 1, x + 1, connect + 1, "diaup")
            return connect

        if direction == "diadown":
            if x < 7 and y > 1:
                if board.coords[y - 1, x + 1] == player:
                    return walk_neighbour(board, player, y - 1, x + 1, connect + 1, "diadown")
            return connect
    return connect


def minmax_recursive(move, board, depth, maxdepth, player):
    copyboard = board.copy()
    points = []
    if player == "X":
        copyboard.make_play(move, "X")
    else:
        copyboard.make_play(move, "O")

    winnersign = find_winner(copyboard)
    if winnersign == "X":
        return 10
    if winnersign == "O":
        return -10

    if depth >= maxdepth:
        return 0

    for move in board.possible_moves():
        if player == "X":
            points.append(minmax_recursive(move, copyboard, depth + 1, maxdepth, "O"))
        else:
            points.append(minmax_recursive(move, copyboard, depth + 1, maxdepth, "X"))

    if player == "O":
        return max(points)
    else:
        return min(points)


def make_aimove(board, maxdepth):
    movescoredict = {}
    for move in board.possible_moves():
        copyboard = board.copy()
        movescoredict[move] = minmax_recursive(move, copyboard, 0, maxdepth, "X")
    # Can't do this cuck with nested lists :/
    print(movescoredict)
    highestscore = max(movescoredict.values())
    highscorekey = random.choice([k for k, v in movescoredict.items() if v == highestscore])

    print("AI played:", highscorekey, end="")
    board.make_play(highscorekey, "X")
    return board


def main():
    b = Board()
    winner = None
    b.print()
    while b.possible_moves():

        playerpos = input("Choose a row to play(1-7): ")
        b.make_play(int(playerpos), "O")
        b.print()
        if find_winner(b):
            break
        print("The AI is thinking .............. :")
        t = time.process_time()
        b = make_aimove(b, 5)
        elapsed_time = time.process_time() - t
        print(" - calc time needed:", elapsed_time)
        b.print()
        if find_winner(b):
            break


main()
