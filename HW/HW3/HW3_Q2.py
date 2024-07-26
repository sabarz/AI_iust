

class sudoku:
    def __init__(self , dim , fileDir) :
        self.dim = 9
        self.expandedNodes = 0
        with open(fileDir) as f:
            content = f.readlines()
            self.board = [list(x.strip()) for x in content]
        self.rv = self.getRemaningValues()

################################################################

    def getDomain(self , row , col):
        RVCell = [str(i) for i in range(1 , self.dim + 1)]
        
        for i in range(self.dim):
            if(self.board[row][i] != '0'):
                if(self.board[row][i] in RVCell):
                    RVCell.remove(self.board[row][i])

        for i in range(self.dim):
            if(self.board[i][col] != '0'):
                if(self.board[i][col] in RVCell):
                    RVCell.remove(self.board[i][col])

        boxRow = row - row % 3
        boxCol = col - col % 3

        for i in range(3):
            for j in range(3) :
                if(self.board[boxRow + i][boxCol + j] != '0'):
                    if(self.board[boxRow + i][boxCol + j] in RVCell):
                        RVCell.remove(self.board[boxRow + i][boxCol + j])

        return RVCell

################################################################

    def getRemaningValues(self) :
        RV = []
        for row in range(self.dim):
            for col in range(self.dim):
                if(self.board[row][col] != '0'):
                    RV.append(['x'])
                else :
                    RV.append(self.getDomain(row , col))
        return RV
#################################################################

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
        
##################################################################

    def SolveSimpleBackTracking(self) :
            location = []
            location = self.getNextLocation()
            if(location[0] == -1):
                return True
            else :
                self.expandedNodes += 1
                for choice in self.rv[location[0] * 9 + location[1]]:
                    self.board[location[0]][location[1]] = str(choice)
                    self.rv = self.getRemaningValues()
                    if(self.SolveSimpleBackTracking()) :
                        return True
                    self.board[location[0]][location[1]] = '0'
            return False

##################################################################
s = sudoku(9 , "jadval.txt")

if(s.SolveSimpleBackTracking()):
    for i in range(9) :
        for j in range(9) :
            print(s.board[i][j] , end=" ")
        print()