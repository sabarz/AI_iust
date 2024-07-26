import gymnasium as gym
import numpy as np
import os.path
import math
import cv2
import random
import matplotlib.pyplot as plt

Q = {}
StateQ = []
LimitLen = 10
TestMode = False
epsilon = 0.1
last_epsilon = 0.05
gamma = 1
alpha = 0.2
ACTIONS = [0, 2, 3]

# def convertToString(image):
#     res = ""
#     for i in range(len(image)):
#         for j in range(len(image[i])):
#             res = res + str(image[i][j])
#     return res
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
    

def CompressImage(image):
	image_data = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	# image_data[image_data > 0] = 1
	# image_data = np.reshape(image_data,(84, 84, 1))
	return image_data

def SaveQ():
    print(len(Q))
    with open("QInfos.txt", 'w') as f:
        for key, value in Q.items():
            f1, f2, f3, action = key
            f.write('%f %f %f %d %f\n' % (f1, f2, f3, action, value))

def ReadQ():
    if (os.path.exists("QInfos.txt")):
        with open("QInfos.txt", 'r') as f:
            for line in f.readlines():
                f1, f2, f3, action, value = line.split()
                Q[(float(f1), float(f2), float(f3), int(action))] = float(value)

def hasGameStarted(state):
    v_pos = state[93:188,8:-8]
    x, y = np.where(v_pos==v_pos.max())
    if state[x[0], y[0]] == 0:
        return False
    return True
    # for i in range(91, 188):
    #     for j in range(len(state[i])):
    #         if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
    #             True
    # return False

def BallPos(state):
    v_pos = state[93:len(state),8:-8]
    x, y = np.where(v_pos==v_pos.max())
    if state[x[0], y[0]] == 0:
        return 0, 0
    return 93 + x[0], 8 + y[0]
    # for i in range(91, len(state)):
    #     for j in range(len(state[i])):
    #         if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
    #             return i, j
    # return 0, 0

def PlatePos(state, action):
    dy = 0
    if action == 3:
        dy = -10
    if action == 2:
        dy = 10
    v_pos = state[191:193,8:-8]
    x, y = np.where(v_pos==v_pos.max())
    return 191 + x[0], 8 + dy + y[0] + 8
    # for i in range(191, 193):
    #     for j in range(len(state[i])):
    #         if state[i][j][0] == 200 and state[i][j][1] == 72 and state[i][j][2] == 72:
    #             return i, dy + j + 8

def BallPlateDistance(state, action):
    x1, y1 = BallPos(state)
    x2, y2 = PlatePos(state, action)
    # print("ball x y: ", action, x1, y1)
    # print("palte x y: ", action, x2, y2)
    return round(abs(x2 - x1) / 4), round(abs(y2 - y1) / 4)

def GetAngel(state, prev_state):
    x1, y1 = BallPos(prev_state)
    x2, y2 = BallPos(state)
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        return 0
    ang = dy / dx
    if ang == 0:
        return 0
    elif ang < 0:
        return -1
    else:
        return 1

def GetFeatures(state, action, prev_state):
    dx, dy = BallPlateDistance(state, action)
    ang = GetAngel(state, prev_state)
    return dx, dy, ang, action

env = None
if TestMode:
    env = gym.make("ALE/Breakout-v5", render_mode="human")
else:
    env = gym.make("ALE/Breakout-v5")

state , info = env.reset(seed=42)
state = CompressImage(state)
#ReadQ()
# print(len(Q))
ah = 0
for episodeNumber in range(1000):
    if not TestMode:
        if episodeNumber % 2000 == 0:
            print(episodeNumber, len(Q))
    StateQ.append(state)
    if len(StateQ) == LimitLen:
        StateQ.pop(0)
    prev_state = state
    if len(StateQ) >= 2:
        prev_state = StateQ[len(StateQ) - 2]
    action = None
    if hasGameStarted(state):
        r = -1 * math.inf
        for a in ACTIONS:
            if GetFeatures(state, a, prev_state) in Q:
                val = Q[GetFeatures(state, a, prev_state)]
                if r < val:
                    r = val
                    action = a

    if action is None or (random.random() <= epsilon and not TestMode):
        action = env.action_space.sample()
    next_state , reward , terminated , truncated , info = env.step(action)
    next_state = CompressImage(next_state)
  
    ah += reward
    lreward.append(ah)
    laction.append(action)
    ltime.append(episodeNumber)
    if not TestMode:
        features = GetFeatures(state, action, prev_state)
        if not features in Q:
            Q[features] = 0.0
        # if Q[features] != 0.0:
        #     print("Action: ", action, "  Q(state, action)", Q[features])

        futureReward = 0
        for a in ACTIONS:
            if GetFeatures(next_state, a, state) in Q:
                futureReward = max(futureReward, Q[GetFeatures(next_state, a, state)])

        Q[features] = (1 - alpha) * Q[features] + alpha * (reward + gamma * futureReward)
        if epsilon >= last_epsilon:
            epsilon -= 0.00005
    # print(len(img_gray), len(img_gray[0]))
    # for i in range(len(img_gray)):
    #     for j in range(len(img_gray[i])):
    #         print(img_gray[i][j], end=" ")
    #     print()
    # print()
    state = next_state
    if terminated or truncated:
        next_state , info = env.reset()
    

#SaveQ()
draw_3D_chart()
env.close()