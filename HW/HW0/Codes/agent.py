from msilib.schema import Condition
from operator import truediv
from pickle import FALSE
import random

#################################################################################
#https://drive.google.com/file/d/1h7e2oNRAgUdMc7i87A0X62CgY0412u9C/view?usp=sharing
#################################################################################

def ai_action(game_state):
    ''' Generate and play move from tic tac toe AI'''
    #################################################################################
    # "*** YOUR CODE HERE ***"
    global condition 
    condition = [
            # horizontal
            (game_state[0], game_state[1], game_state[2], game_state[3]),
            (game_state[1], game_state[2], game_state[3], game_state[4]),
            (game_state[5], game_state[6], game_state[7], game_state[8]),
            (game_state[6], game_state[7], game_state[8], game_state[9]),
            (game_state[10], game_state[11], game_state[12], game_state[13]),
            (game_state[11], game_state[12], game_state[13], game_state[14]),
            (game_state[15], game_state[16], game_state[17], game_state[18]),
            (game_state[16], game_state[17], game_state[18], game_state[19]),
            (game_state[20], game_state[21], game_state[22], game_state[23]),
            (game_state[21], game_state[22], game_state[23], game_state[24]),

            # vertical
            (game_state[0], game_state[5], game_state[10], game_state[15]),
            (game_state[5], game_state[10], game_state[15], game_state[20]),
            (game_state[1], game_state[6], game_state[11], game_state[16]),
            (game_state[6], game_state[11], game_state[16], game_state[21]),
            (game_state[2], game_state[7], game_state[12], game_state[17]),
            (game_state[7], game_state[12], game_state[17], game_state[22]),
            (game_state[3], game_state[8], game_state[13], game_state[18]),
            (game_state[8], game_state[13], game_state[18], game_state[23]),
            (game_state[4], game_state[9], game_state[14], game_state[19]),
            (game_state[9], game_state[14], game_state[19], game_state[24]),

            # diagonal
            (game_state[0], game_state[6], game_state[12], game_state[18]),
            (game_state[6], game_state[12], game_state[18], game_state[24]),
            (game_state[4], game_state[8], game_state[12], game_state[16]),
            (game_state[8], game_state[12], game_state[16], game_state[20]),
            (game_state[1], game_state[7], game_state[13], game_state[19]),
            (game_state[5], game_state[11], game_state[17], game_state[23]),
            (game_state[3], game_state[7], game_state[11], game_state[15]),
            (game_state[9], game_state[13], game_state[17], game_state[21]),

        ]

    global indexes 
    indexes = [
        (0 , 1 , 2 , 3) ,
        (1 , 2 , 3 , 4) ,
        (5 , 6 , 7 , 8) ,
        (6 , 7 , 8 , 9) ,
        (10 , 11 , 12 , 13) , 
        (11 , 12 , 13 , 14) ,
        (15 , 16 , 17 , 18) , 
        (16 , 17 , 18 , 19) ,
        (20 , 21 , 22 , 23) ,
        (21 , 22 , 23 , 24) , 
        (0 , 5 , 10 , 15) ,
        (5 , 10 , 15 , 20) ,
        (1 , 6 , 11 , 16) , 
        (6 , 11 , 16 , 21) ,
        (2 , 7 , 12 , 17) , 
        (7 , 12 , 17 , 22) ,
        (3 , 8 , 13 , 18) ,
        (8 , 13 , 18 , 23) ,
        (4 , 9 , 14 , 19) ,
        (9 , 14 , 19 , 24) ,
        (0 , 6 , 12 , 18) ,
        (6 , 12 , 18 , 24) ,
        (4 , 8 , 12 , 16) ,
        (8 , 12 , 16 , 20) ,
        (1 , 7 , 13 , 19) ,
        (5 , 11 , 17 , 23) ,
        (3 , 7 , 11 , 15) ,
        (9 , 13 , 17 , 21) ,
    ]

    global important_indexes 
    important_indexes = [6 , 7 , 8 , 11 , 12 , 13 , 16 , 17 , 18]
  
    j = 0
    for i in condition :
        if i == (False , False , False , None) :
            return indexes[j][3]
        elif i == (False , False , None , False) :
            return indexes[j][2]
        elif i == (False , None , False , False) : 
            return indexes[j][1]
        elif i == (None , False , False , False) : 
            return indexes[j][0]
        elif i == (True , True , True , None) : 
            return indexes[j][3]
        elif i == (True , True , None , True) :
            return indexes[j][2]
        elif i == (True , None , True , True) : 
            return indexes[j][1]
        elif i == (None , True , True , True) : 
            return indexes[j][0]  
        j+=1

    j = 0
    for i in condition :
        if i == (False , False , False , None) :
            return indexes[j][3]
        elif i == (False , False , None , False) :
            return indexes[j][2]
        elif i == (False , None , False , False) : 
            return indexes[j][1]
        elif i == (None , False , False , False) : 
            return indexes[j][0]
        elif i == (True , True , True , None) : 
            return indexes[j][3]
        elif i == (True , True , None , True) :
            return indexes[j][2]
        elif i == (True , None , True , True) : 
            return indexes[j][1]
        elif i == (None , True , True , True) : 
            return indexes[j][0]  
        j+=1

    j = 0
    for i in condition :
        if i == (None , True , True , None) : 
            return indexes[j][0]
        j += 1

    j = 0
    for i in condition :
        if i == (None , False , False , None) and important_indexes.count(indexes[j][0]) == 1:
            return indexes[j][0]
        elif i == (None , False , False , None) and important_indexes.count(indexes[j][3]) == 1:
            return indexes[j][3]
        elif i == (False , False , None , None) and important_indexes.count(indexes[j][2]) == 1:
            return indexes[j][2]
        elif i == (False , False , None , None) and important_indexes.count(indexes[j][3]) == 1:
            return indexes[j][3]
        elif i == (None , False , None , False) and important_indexes.count(indexes[j][0]) == 1:
            return indexes[j][0]
        elif i == (None , False , None , False) and important_indexes.count(indexes[j][2]) == 1:
            return indexes[j][2]
        elif i == (None , None , False , False) and important_indexes.count(indexes[j][0]) == 1:
            return indexes[j][0]
        elif i == (None , None , False , False) and important_indexes.count(indexes[j][1]) == 1:
            return indexes[j][1]
        elif i == (False , None , False , None) and important_indexes.count(indexes[j][1]) == 1:
            return indexes[j][1]
        elif i == (False , None , False , None) and important_indexes.count(indexes[j][3]) == 1:
            return indexes[j][3]
        elif i == (False , None , None , False) and important_indexes.count(indexes[j][1]) == 1:
            return indexes[j][1]
        elif i == (False , None , None , False) and important_indexes.count(indexes[j][2]) == 1:
            return indexes[j][2]
        j+=1

    j = 0
    for i in condition :
        if i == (None , False , None , None) and important_indexes.count(indexes[j][0]) == 1 :
            return indexes[j][0]
        elif i == (None , False , None , None) and important_indexes.count(indexes[j][2]) == 1:
            return indexes[j][2]
        elif i == (None , False , None , None) and important_indexes.count(indexes[j][3]) == 1:
            return indexes[j][3]
        elif i == (None , None , False , None) and important_indexes.count(indexes[j][0]) == 1:
            return indexes[j][0]
        elif i == (None , None , False , None) and important_indexes.count(indexes[j][1]) == 1 :
            return indexes[j][1]
        elif i == (None , None , False , None) and important_indexes.count(indexes[j][3]) == 1 :
            return indexes[j][3]
        elif i == (None , None , None , False) and important_indexes.count(indexes[j][0]) == 1 :
            return indexes[j][0]
        elif i == (None , None , None , False) and important_indexes.count(indexes[j][1]) == 1 :
            return indexes[j][1]
        elif i == (None , None , None , False) and important_indexes.count(indexes[j][2]) == 1 :
            return indexes[j][2]
        elif i == (False , None , None , None) and important_indexes.count(indexes[j][1]) == 1 :
            return indexes[j][1]
        elif i == (False , None , None , None) and important_indexes.count(indexes[j][2]) == 1 :
            return indexes[j][2]
        elif i == (False , None , None , None) and important_indexes.count(indexes[j][3]) == 1 :
            return indexes[j][3]
        j += 1

    hi = None 
    if game_state[12] == None :
            return 12
    else :
        while(hi == None):
            hi2 = random.choice([6 , 7 , 8 , 11 , 13 , 16 , 17 , 18])
            hi = game_state[hi2]
            return hi2 
    hi = None
    while(hi == None):
            hi2 = random.choice(range(0 , 25))
            hi = game_state[hi2]
            return hi2 
    #################################################################################
    pass
    