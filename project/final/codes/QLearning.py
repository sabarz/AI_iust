import gymnasium as gym
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

Q = {}
gamma = 1
alpha = 0.2
last_epsilon = 0.05
epsilon = 0.1
ACTIONS = [0, 2, 3]

laction = []
lreward = []
ltime=[]

def draw_3D_chart():
    #fig = plt.figure()
    plt.xlabel('Action')
    plt.ylabel('Reward')
    plt.plot(np.array(laction),np.array(lreward),label='Room 1 Temperature at Mehr',marker='o')
    plt.legend()
    plt.show()


    
def convertToString(image):
    res = ""
    for i in range(len(image)):
        for j in range(len(image[i])):
            res = res + str(image[i][j])
    return res

def CompressImage(image):
	image_data = cv2.cvtColor(cv2.resize(image, (84, 84)), cv2.COLOR_BGR2GRAY)
	image_data[image_data > 0] = 1
	# image_data = np.reshape(image_data,(84, 84, 1))
	return convertToString(image_data)

def SaveQ():
    with open("QInfos.txt", 'w') as f:
        for key, value in Q.items():
            state, action = key
            f.write('%s %d %f\n' % (state, action, value))

def ReadQ():
    with open("QInfos.txt", 'r') as f:
        for line in f.readlines():
            state, action, value = line.split()
            Q[(state, int(action))] = float(value)


env = gym.make("ALE/Breakout-v5", render_mode="human")
# env = gym.make("ALE/Breakout-v5")
state , info = env.reset(seed=42)
state = CompressImage(state)
ReadQ()
# print(len(Q))

ah = 0
for i in range(2000):
    action = None
    r = 0
    for a in ACTIONS:
        if (state, a) in Q and r < Q[(state, a)]:
            r = Q[(state, a)]
            action = a
    if action is None or random.random() <= epsilon:
        action = env.action_space.sample()
    next_state , reward , terminated , truncated , info = env.step(action)
    next_state = CompressImage(next_state)
   
    ah += reward
    lreward.append(ah)
    laction.append(action)
    if not (state, action) in Q:
        Q[(state, action)] = 0.0
    
    if Q[((state, action))] != 0.0:
        print("Action: ", action, "  Q(state, action)", Q[((state, action))])

    futureReward = 0
    for a in ACTIONS:
        if (next_state, action) in Q:
            futureReward = max(futureReward, Q[(next_state, action)])

    Q[(state, action)] = (1 - alpha) * Q[(state, action)] + alpha * (reward + gamma * futureReward)

    if epsilon > last_epsilon:
        epsilon -= 0.001
    # print(len(img_gray), len(img_gray[0]))
    # for i in range(len(img_gray)):
    #     for j in range(len(img_gray[i])):
    #         print(img_gray[i][j], end=" ")
    #     print()
    # print()
    state = next_state
    if terminated or truncated:
        next_state , info = env.reset()
SaveQ()
draw_3D_chart()
env.close()