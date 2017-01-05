import random, time

canicount = 0

class Board:
    def __init__(self):
        self.coords = {}
        self.clear()

    def clear(self):
        for y in range(1, 7):
            for x in range(1, 8):
                self.coords[x, y] = "-"

    def row_isfull(self, position):
        for y in range(1, 7):
            if self.coords[position, y] == "-":
                return False
        return True

    def print(self):
        print("")
        for y in range(6, 0, -1):
            print(y, end=" ")
            for x in range(1, 8):
                print(self.coords[x, y], end=" ")
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
            if self.coords[position, y] == "-":
                self.coords[position, y] = sign
                placed = True
                break
                # if not placed:
                #    print("Board is full on column: " + str(position))

    def copy(self):
        newboard = Board()
        newboard.coords = {k: v for k, v in self.coords.items()}
        return newboard


def calc_row(board, start, player):
    stop = {
        "x": start['x'],
        "y": start['y'],
    }

    for startend in range(3):
        start["x"] = start["x"] - 1 if start["x"] > 1 else start["x"]
        stop["x"] = stop["x"] + 1 if stop["x"] < 7 else stop["x"]

    connecttemp = 0
    connected = 0
    total = 0
    for x in range(start["x"], stop["x"] + 1):
        if board.coords[x, stop["y"]] == player:
            connecttemp += 1
            total += 1
        else:
            connecttemp = 0

        connected = connecttemp if connecttemp > connected else connected

    return [connected, total]


def calc_col(board, start, player):
    stop = {
        "x": start['x'],
        "y": start['y'],
    }

    for startend in range(3):
        start["y"] = start["y"] - 1 if start["y"] > 1 else start["y"]

    connecttemp = 0
    connected = 0
    total = 0
    for y in range(start["y"], stop["y"] + 1):
        if board.coords[start['x'], y] == player:
            connecttemp += 1
            total += 1

        else:
            connecttemp = 0
        connected = connecttemp if connecttemp > connected else connected

    return [connected, total]


def calc_diaup(board, start, player):
    stop = {
        "x": start['x'],
        "y": start['y'],
    }

    for startend in range(3):
        if start['x'] > 1 and start['y'] > 1:
            start["x"] -= 1
            start["y"] -= 1

        if stop['x'] < 7 and stop['y'] < 6:
            stop['x'] += 1
            stop['y'] += 1

    connecttemp = 0
    connected = 0
    total = 0
    for walk in range((stop["y"] - start['y']) + 1):  # vereinfachen?
        if board.coords[start['x'] + walk, start['y'] + walk] == player:
            connecttemp += 1
            total += 1

        else:
            connecttemp = 0
        connected = connecttemp if connecttemp > connected else connected

    return [connected, total]


def calc_diadown(board, start, player):
    stop = {
        "x": start['x'],
        "y": start['y'],
    }

    for startend in range(3):
        if start['x'] > 1 and start['y'] > 6:
            start["x"] -= 1
            start["y"] -= 1

        if stop['x'] < 7 and stop['y'] > 1:
            stop['x'] += 1
            stop['y'] -= 1

    connecttemp = 0
    connected = 0
    total = 0
    for walk in range((stop["x"] - start['x']) + 1):  # vereinfachen?
        if board.coords[start['x'] + walk, start['y'] - walk] == player:
            connecttemp += 1
            total += 1

        else:
            connecttemp = 0
        connected = connecttemp if connecttemp > connected else connected

    return [connected, total]


def find_winner(board, move):
    player = None
    y = None
    x = move
    for searchy in range(1, 7):
        if board.coords[move, searchy] != "-":
            player = board.coords[move, searchy]
            y = searchy
        else:
            break
    """
    print("Checking Player:",player, "("+str(x)+","+str(y)+")")
    print("row:",calc_row(board,{"x": x,"y": y},player))
    print("col:",calc_col(board,{"x": x,"y": y},player))
    print("diaup:", calc_diaup(board,{"x": x,"y": y},player))
    print("diadown:", calc_diadown(board,{"x": x,"y": y},player))
    """
    # todo: dict übergabe verbessern

    scores = []

    scores.append(calc_row(board, {"x": x, "y": y}, player))
    scores.append(calc_col(board, {"x": x, "y": y}, player))
    scores.append(calc_diaup(board, {"x": x, "y": y}, player))
    scores.append(calc_diadown(board, {"x": x, "y": y}, player))

    connected = 0
    total = 0
    for score in scores:
        if score[0] == 4:
            return 1000
        connected += score[0]
        total += score[1]

    return total + connected * 3


def minmax_recursive(move, board, depth, maxdepth, player):
    global canicount
    copyboard = board.copy()
    canicount += 1
    points = []
    if player == "X":
        copyboard.make_play(move, "X")
    else:
        copyboard.make_play(move, "O")

    score = find_winner(copyboard, move)

    if score == 1000:
        if player == "X":
            return score
        if player == "O":
            return score * -1

    if depth == maxdepth:
        return score

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
    global canicount

    while b.possible_moves():
        playerpos = input("Choose a row to play(1-7): ")
        b.make_play(int(playerpos), "O")
        b.print()
        print("The AI is thinking .............. :")
        t = time.process_time()
        b = make_aimove(b, 5)
        elapsed_time = time.process_time() - t
        print(" - calc time:", elapsed_time, "-", canicount, "total calculations")
        canicount = 0
        b.print()
main()


# @line 261 - AI Recursive depth
# @line 198 - AI Move Score Weighting
# game does not end yet