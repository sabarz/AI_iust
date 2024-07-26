from os import stat
from random import randrange
from selectors import SelectorKey
from tkinter import E


class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        if(self.value(state) == 0):
            return True
        else:
            return False

    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        counter = 0
        seen = []
        for item in state :
            if (item in seen):
                counter += 1
            else:
                seen.append(item)
        
        for i in range(0 , self.N):
            for j in range(i + 1 , self.N):
                if(abs(i - j) == abs(state[i] - state[j])):
                    counter += 1

        return counter

    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        newState = []

        for i in range(0 , self.N):
            for j in range(0 , self.N):
                idk = []
                if(j != state[i]):
                    idk.insert(i , j)
                    for t in range(0 , self.N):
                        if(t != i):
                            idk.insert(t , state[t])
                
                    newState.append(tuple(idk))
            
        return newState