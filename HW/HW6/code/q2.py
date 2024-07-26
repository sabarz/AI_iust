from copy import copy, deepcopy
from ctypes.wintypes import HLOCAL
import math
from random import choice
import os
from tkinter import SEL

from numpy import true_divide

player, opponent = 'X', 'O'
#1 computer
#0 player
class Nodes:
    def __init__(self , b , p , s , t):
        self.visit = 0
        self.win = 0
        self.uct = 0
        self.board = b
        self.child = []
        self.parent = p
        self.space = s
        self.turn = t

def findneighbors(r):
    ans = []
    for i in range(3):
        for j in range(3):
            if(r.board[i][j] == '_'):  
                hold = [['_'] * 3] * 3 
                hold = deepcopy(r.board)
                hold[i][j] = 'O'
                ans.append(Nodes(hold , r , r.space - 1 , 1))
    return ans

def selection(r):
    while(len(r.child) != 0 and len(r.child) == r.space):
        hi = -999999
        for i in r.child:
            if hi < i.uct:
                hi = i.uct
        for x in r.child:
            if(x.uct == hi):
                r = x
                break
    expantion(r)

def expantion(r):
    for i in range(3):
        for j in range(3):
            if(r.board[i][j] == '_'):
                flag = True
                for x in r.child:
                    if(x.board[i][j] != '_'):
                        flag = False
                if flag:
                    hold =  [['_'] * 3] * 3 
                    if(r.turn == 0):
                        hold = deepcopy(r.board)
                        hold[i][j] = 'O'
                        hey = Nodes(hold , r , r.space - 1 , 1)
                        r.child.append(hey)
                        Backpropagation(hey)
                        return 
                    else:
                        hold = deepcopy(r.board)
                        hold[i][j] = 'X'
                        hey = Nodes(hold , r , r.space - 1 , 0)
                        r.child.append(hey)
                        Backpropagation(hey)
                        return

def findRandom(board):
    empty_spots = [i*3+j for i in range(3)
        for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return[int(idx/3), idx % 3]
    

def isMovesLeft(board):
    return ('_' in board[0] or '_' in board[1] or '_' in board[2])


def simulation(b):
    board = deepcopy(b)
    compterturn = False
    while(isMovesLeft(board)):
        index = findRandom(board)
        if(compterturn):
            board[index[0]][index[1]] = 'O'
            compterturn = False
        else:
            board[index[0]][index[1]] = 'X'
            compterturn = True
    
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][0] == 'O'):
            return 1
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] == 'O'):
            return 1

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] == 'O'):
        return 1

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] == 'O'):
        return 1
    
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][0] == 'X'):
            return 0
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] == 'X'):
            return 0

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] == 'X'):
        return 0

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] == 'X'):
        return 0
    return 3

def Backpropagation(r):
    hi = simulation(deepcopy(r.board))
    while(r.parent != None):
        if(hi == 3):
            r.visit += 1
        elif(hi != r.turn):
            r.win -= 1
            r.visit += 1
        else:
            r.win += 1
            r.visit += 1
        r.uct = (r.win / r.visit) + (1.5 * (math.sqrt((math.log(r.parent.visit) / r.visit))))
        for x in r.child:
            x.uct = (x.win / x.visit) + (1.5 * (math.sqrt((math.log(r.visit) / x.visit))))
        r = r.parent
    r.visit += 1

    
def findBestMove(board):
    jizz = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] == '_'):
                jizz += 1
    root = Nodes(board , None , jizz , 0)
    root.child = findneighbors(root)
    for i in root.child:
        if(simulation(i.board) == 1):
            root.visit += 1
            i.visit += 1
            i.win += 1
            i.uct = (i.win / i.visit) + (1.5 * (math.sqrt((math.log(root.visit) / i.visit))))
        elif(simulation(i.board) == 0):
            root.visit += 1
            i.visit += 1
            i.win -= 1
            i.uct = (i.win / i.visit) + (1.5 * (math.sqrt((math.log(root.visit) / i.visit))))
        else:
            root.visit += 1
            i.visit += 1
            i.uct = (i.win / i.visit) + (1.5 * (math.sqrt((math.log(root.visit) / i.visit))))

    for iteration in range(1000):
        selection(root)

    hi = -9999999
    nmd = Nodes(None, None , None , None)
    for i in root.child:
        if hi < i.uct:
            hi = i.uct
    for x in root.child:
        if(x.uct == hi):
            nmd = x
            break

    #if(board[0][0] == 'X' and board[2][2] == 'X'):
    #    return [1 , 1]

    for i in range(3):
        for j in range(3):
            if(board[i][j] != nmd.board[i][j]):
                return[i , j]

def checkWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return True

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return True

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return True

    return False


def printBoard(board):
    os.system('cls||clear')
    print("\n Player : X , Agent: O \n")
    for i in range(3):
        print(" ", end=" ")
        for j in range(3):
            if(board[i][j] == '_'):
                print(f"[{i*3+j+1}]", end=" ")
            else:
                print(f" {board[i][j]} ", end=" ")

        print()
    print()


if __name__ == "__main__":
    board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
    ]

    turn = 0

    while isMovesLeft(board) and not checkWin(board):
        if(turn == 0):
            printBoard(board)
            print(" Select Your Move :", end=" ")
            tmp = int(input())-1
            userMove = [int(tmp/3),  tmp % 3]
            while((userMove[0] < 0 or userMove[0] > 2) or (userMove[1] < 0 or userMove[1] > 2) or board[userMove[0]][userMove[1]] != "_"):
                print('\n \x1b[0;33;91m' + ' Invalid move ' + '\x1b[0m \n')
                print("Select Your Move :", end=" ")
                tmp = int(input())-1
                userMove = [int(tmp/3),  tmp % 3]
            board[userMove[0]][userMove[1]] = player
            print("Player Move:")
            printBoard(board)
            turn = 1
        else:
            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = opponent
            print("Agent Move:")
            printBoard(board)
            turn = 0

    if(checkWin(board)):
        if(turn == 1):
            print('\n \x1b[6;30;42m' + ' Player Wins! ' + '\x1b[0m')

        else:
            print('\n \x1b[6;30;42m' + ' Agent Wins! ' + '\x1b[0m')
    else:
        print('\n \x1b[0;33;96m' + ' Draw! ' + '\x1b[0m')

    input('\n Press Enter to Exit... \n')
