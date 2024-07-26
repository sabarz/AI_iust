import gymnasium as gym
import numpy as np
import os.path
import cv2
import random
import math

gamma = 1
alpha = 0.2
last_epsilon = 0.05
epsilon = 0.05
Limit = 1000 * 1000
ACTIONS = [0, 2, 3]
W1 = 0
W2 = 0
W3 = 0

def SaveQ():
    with open("WInfos.txt", 'w') as f:
        f.write('%f %f %f\n' % (W1, W2, W3))

def ReadQ():
    if (os.path.exists("WInfos.txt")):
        with open("WInfos.txt", 'r') as f:
            line = f.readline()
            W1, W2, W3 = line.split()
            return float(W1), float(W2), float(W3)
    return 0, 0, 0

def hasGameStarted(state):
    for i in range(91, 188):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                True
    return False

def BallPos(state):
    for i in range(91, len(state)):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                return i, j
    return 0, 0

def PlatePos(state, action):
    dy = 0
    if action == 3:
        dy = -10
    if action == 2:
        dy = 10
    for i in range(191, 193):
        for j in range(len(state[i])):
            if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
                return i, dy + j + 8

def BallPlateDistance(state, action):
    x1, y1 = BallPos(state)
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

def f(state, action):
    dx, dy = BallPlateDistance(state, action)
    return W1 * dx + W2 * dy + W3 * BreakCount(state)

env = gym.make("ALE/Breakout-v5", render_mode="human")
# env = gym.make("ALE/Breakout-v5")
state , info = env.reset(seed=42)
W1, W2, W3 = ReadQ()
# print(len(Q))

for mamd in range(3000):
    if mamd % 50 == 0:
        print(mamd, W1, W2, W3)
    action = None
    r = -1 * math.inf
    # print("\n=====================================\n")
    if hasGameStarted(state):
        for a in ACTIONS:
            val = f(state, a)
            # print("val: ", a, val)
            if r < val:
                r = val
                action = a

    if action is None or random.random() <= epsilon:
        action = env.action_space.sample()
    # print(action, W1, W2, W3, end = " ||||| ")
    next_state , reward , terminated , truncated , info = env.step(action)
    # print("reward: ", reward)
    # print("=====================================\n")
    # print(PlatePos(next_state), end = " ")
    # img_gray = next_state
    # i, j = PlatePos(next_state)
    # img_gray[i][j] = [255, 255, 0]
    # img_gray = cv2.resize(img_gray, (420, 320))
    # for i in range(0, len(img_gray)):
    #     if 55 <= i <= 91:
    #         continue
    #     for j in range(len(img_gray[i])):
    #         img_gray[i][j] = [123, 123, 123]
    # cv2.imshow('image', img_gray)

    futureReward = 0
    for a in ACTIONS:
        futureReward = max(futureReward, f(next_state, a))
    difference = (reward + gamma * futureReward) - f(state, action)
    dx, dy = BallPlateDistance(state, action)
    W1 = round(W1 + alpha * difference * dx, 6)
    W2 = round(W2 + alpha * difference * dy, 6)
    W3 = round(W3 + alpha * difference * BreakCount(state), 6)
    # while abs(W1) > Limit or abs(W2) > Limit or abs(W3) > Limit:
    #     W1 = round(W1 / 100, 3)
    #     W2 = round(W2 / 100, 3)
    #     W3 = round(W3 / 100, 3)
    # if W1 != 0:
    #     print(W1, W2, W3, difference, reward, futureReward)
    #     exit()
    state = next_state
    if terminated or truncated:
        next_state , info = env.reset()
SaveQ()
env.close()