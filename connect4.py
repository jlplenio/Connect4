# coding=UTF8
from random import randint

board = {}

def isfull(position):
    for y in range(1,7):
        if board[y,position] == "-":
            return False
    return True

def initboard():
    for y in range(1, 7):
        for x in range(1, 8):
            board[y, x] = "-"

def printBoard():
    print("1", "2", "3", "4", "5", "6", "7")
    for y in range(6, 0, -1):
        for x in range(1, 8):
            print(board[y, x], end=" ")
        print()
    print()

def makePlay(position, sign):
    set = False
    for y in range(1, 7):
        if board[y, position] == "-":
            board[y, position] = sign
            set = True
            break
    if not set:
        print("Board is full on column: " + str(position))

def findWinner(player):
    found = False
    for y in range(1, 7):
        for x in range(1, 8):
            if board[y, x] == player:
                if walkNeighbor(player, y, x, 1, "right") == 4:
                    print(str(y) + "-" + str(x) + " Winner going right - Player "+player)
                    found = True
                elif walkNeighbor(player, y, x, 1, "up") == 4:
                    print(str(y) + "-" + str(x) + " Winner going up - Player "+player)
                    found = True
                elif walkNeighbor(player, y, x, 1, "diaup") == 4:
                    print(str(y) + "-" + str(x) + " Winner going diagonal up - Player "+player)
                    found = True
                elif walkNeighbor(player, y, x, 1, "diadown") == 4:
                    print(str(y) + "-" + str(x) + " Winner going diagonal down - Player "+player)
                    found = True
                break
    return found

def walkNeighbor(player, y, x, connect, direction):
    if connect != 4:
        if direction == "right":
            if x < 7:
                if board[y, x + 1] == player:
                    return walkNeighbor(player, y, x + 1, connect + 1, "right")

        if direction == "up":
            if y < 6:
                if board[y + 1, x] == player:
                    return walkNeighbor(player, y + 1, x, connect + 1, "up")

        if direction == "diaup":
            if x < 7 and y < 6:
                if board[y + 1, x + 1] == player:
                    return walkNeighbor(player, y + 1, x + 1, connect + 1, "diaup")

        if direction == "diadown":
            if x < 7 and y > 1:
                if board[y - 1, x + 1] == player:
                    return walkNeighbor(player, y - 1, x + 1, connect + 1, "diadown")

    return connect

initboard()

player = "X"
won = False
while not won:
    while True:
        #infloop if all columns full
        col = randint(1,7)
        if not isfull(col):
            break
    makePlay(col,player)
    printBoard()
    won = findWinner(player)
    if player == "X":
        player = "O"
    else:
        player = "X"