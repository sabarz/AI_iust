from asyncore import read
from http.client import LENGTH_REQUIRED
import gymnasium as gym
import numpy as np
import os.path
import cv2
import random
import matplotlib.pyplot as plt
import math

Q = []
isTest = False
LimitLen = 10
gamma = 1
alpha = 0.2
epsilon = 0.05
ACTIONS = [0, 2, 3]
W1 = 0
W2 = 0
W3 = 0
W4 = 0


laction = []
lreward = []
ltime=[]

def draw_3D_chart():
    #fig = plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Reward')
    plt.plot(np.array(ltime),np.array(lreward))
    plt.legend()
    plt.show()
    
def SaveW():
    with open("WInfos.txt", 'w') as f:
        f.write('%f %f %f %f\n' % (W1, W2, W3, W4))

def ReadW():
    if (os.path.exists("WInfos.txt")):
        with open("WInfos.txt", 'r') as f:
            line = f.readline()
            W1, W2, W3, W4 = line.split()
            return float(W1), float(W2), float(W3), float(W4)
    return 0, 0, 0, 0

def hasGameStarted(state):
    for i in range(91, 188):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                return True
    return False

def BallPos(state):
    for i in range(91, len(state)):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                return i, j
    return 0, 0

def BallNextPos(state, prev_state):
    x1, y1 = BallPos(prev_state)
    x2, y2 = BallPos(state)
    dx = x2 - x1
    dy = y2 - y1
    return x2 + dx, y2 + dy

def PlatePos(state, action):
    dy = 0
    if action == 3:
        dy = -5
    if action == 2:
        dy = 5
    for i in range(191, 193):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                return i, dy + j + 8

def BallPlateDistance(state, action, prev_state):
    x1, y1 = BallNextPos(state, prev_state)
    x2, y2 = PlatePos(state, action)
    # print("ball x y: ", action, x1, y1)
    # print("palte x y: ", action, x2, y2)
    return abs(x2 - x1) / 100, abs(y2 - y1) / 100

def BreakCount(state):
    cnt = 0
    for i in range(55, 92):
        for j in range(len(state[i])):
            if state[i][j][0] != 0 or state[i][j][1] != 0 or state[i][j][2] != 0:
                cnt += 1
    return cnt / 10000

def BallLandingPosDistance(state, prev_state, action):
    x1, y1 = BallPos(prev_state)
    x2, y2 = BallPos(state)
    xp, yp = PlatePos(state, action)
    dx = x2 - x1
    dy = y2 - y1
    if dx <= 0:
        return 0
    y3 = y2 + dy * ((210 - x2) / dx)
    # print("x1 y1 x2 y2, dx, dy, xp, yp y3: ", x1, y1, x2, y2, dx, dy, xp, yp, y3)
    if y3 < 0:
        y3 = 0
    if (y3 > 160):
        y3 = 160
    return abs(y3 - yp) / 100


def f(state, action, prev_state):
    dx, dy = BallPlateDistance(state, action, prev_state)
    return W1 * dx + W2 * dy + W3 * BreakCount(state) + W4 * BallLandingPosDistance(state, prev_state, action)

env = gym.make("ALE/Breakout-v5", render_mode="human", frameskip=3)
if not isTest:
    env = gym.make("ALE/Breakout-v5", frameskip=3)
state , info = env.reset(seed=42)
W1, W2, W3, W4 = ReadW()
if isTest:
    epsilon = 0
# print(len(Q))

ah = 0
for mamd in range(1000):
    if mamd % 50 == 0:
        print(mamd, W1, W2, W3, W4)

    Q.append(state)
    if len(Q) == LimitLen:
        Q.pop(0)
    prev_state = state
    if len(Q) >= 2:
        prev_state = Q[len(Q) - 2]


    action = None
    r = -1 * math.inf
    if hasGameStarted(state):
        for a in ACTIONS:
            val = f(state, a, prev_state)
            if r < val:
                r = val
                action = a

    if action is None or random.random() <= epsilon:
        action = env.action_space.sample()

    next_state , reward , terminated , truncated , info = env.step(action)
    
    ah += reward
    lreward.append(ah)
    laction.append(action)
    ltime.append(mamd)
    #print(reward , "nmd" , action)

    if not isTest:
        futureReward = 0
        for a in ACTIONS:
            futureReward = max(futureReward, f(next_state, a, state))
        difference = (reward + gamma * futureReward) - f(state, action, prev_state)
        dx, dy = BallPlateDistance(state, action, prev_state)
        W1 = round(W1 + alpha * difference * dx, 6)
        W2 = round(W2 + alpha * difference * dy, 6)
        W3 = round(W3 + alpha * difference * BreakCount(state), 6)
        W4 = round(W4 + alpha * difference * BallLandingPosDistance(state, prev_state, action), 6)


    state = next_state
    if terminated or truncated:
        next_state , info = env.reset()
    if mamd % 1000 == 0:
        SaveW()

draw_3D_chart()
env.close()