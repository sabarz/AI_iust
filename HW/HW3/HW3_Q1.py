from inspect import BoundArguments
import re
from numpy import true_divide


class Sudoku :
    
    def __init__(self, b):
        #self.board = [][]
        self.board = b
        self.expandedNodes = 0
        self.dim = 9

####################################################

    def getNextLocation(self) :
        loc = []
        loc.append(-1)
        loc.append(-1)
        for i in range(9) :
            for j in range(9) :
                if(self.board[i][j] == '0'):
                    loc[0] = i
                    loc[1] = j
                    return loc
        return loc

####################################################

    def isSafe(self , x , y , c):
        for i in range(9) :
            if(self.board[x][i] == str(c) or self.board[i][y] == str(c)):
                return False
        hi1 = (int)(x / 3)
        hi2 = (int)(y / 3)
        for i in range(hi1 * 3 , hi1 * 3 + 3):
            for j in range(hi2 * 3 , hi2 * 3 + 3):
                if(self.board[i][j] == str(c)):
                    return False            
        return True
                
####################################################

    def SolveSimpleBackTracking(self) :
        location = []
        location = self.getNextLocation()
        if(location[0] == -1):
            return True
        else :
            self.expandedNodes += 1
            for choice in range(1, self.dim + 1):
                if(self.isSafe(location[0] , location[1] , choice)):
                    self.board[location[0]][location[1]] = str(choice)
                    if(self.SolveSimpleBackTracking()) :
                        return True
                    self.board[location[0]][location[1]] = '0'
        return False

####################################################
b = [
    ['0' , '1' , '6' , '3' , '0' , '8' , '4' , '2' , '0'],
    ['8' , '4' , '0' , '0' , '0' , '7' , '3' , '0' , '0'],
    ['3' , '0' , '0' , '0' ,'0' , '0' , '0' , '0' , '0'],
    ['0' , '6' , '0' , '9' , '4' , '0' , '8' , '0' , '2'],
    ['0' , '8' , '1' , '0' , '3' , '0' , '7' , '9' , '0'],
    ['9' , '0' , '3' , '0' , '7' , '6' , '0' , '4' , '0'],
    ['0' , '0' , '0' , '0' , '0' , '0' , '0' , '0' , '3'],
    ['0' , '0' , '5' , '7' , '0' , '0' , '0' , '6' , '8'],
    ['0' , '7' , '8' , '1' , '0' , '3' , '2' , '5' , '0'],
]
s = Sudoku(b)
if(s.SolveSimpleBackTracking()):
    for i in range(9) :
        for j in range(9) :
            print(b[i][j] , end=" ")
        print()