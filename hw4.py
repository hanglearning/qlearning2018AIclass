# Hang Chen
# CISC681 hw4 2018F

# This script utilizes recordclass library(https://pypi.org/project/recordclass/)
# which you may not have in your environment.
# Please run '$ pip install recordclass' or '$ pip3 install recordclass' to install,
# or check out an online version of this homework at
# https://repl.it/@hanglearning/681hw4?language=python3
# Please abide by the input format and run with $ python hw4.py <input>
from recordclass import recordclass
import sys
import random

# Settings - you may alternative the settings including the dimensions of the board
ROW = 5
COLUMN = 5
STATE_SPACE = ROW * COLUMN
START_STATE = 1
ITERATIONS = 10000
LIVING_REWARD = -0.1
DISCOUNT_RATE = 0.5
LEARNING_RATE = 0.1
DONUT_REWARD = 100
FORBIDDEN_REWARD = -100
EPSILON = 0.1
EPSILON_CONVERGENCE = 10000

# get user inputs
arguments = sys.argv
donutLoc = int(arguments[1])
forbiddenLoc = int(arguments[2])
wallLoc = int(arguments[3])

# base class for the state
State = recordclass('State', 'stateSequence availableActions qValues isDonut isForbidden isWall')
# states are held in a maze array
maze = []

# initialize the maze with 12 states
for i in range(1, STATE_SPACE + 1):
    state = State(i, [], [0, 0, 0, 0], False, False, False)
    maze.append(state)

# assign the donut, forbidden and wall locations
maze[donutLoc - 1].isDonut = True
maze[forbiddenLoc - 1].isForbidden = True
maze[wallLoc - 1].isWall = True

# justify the wall location to see if the going state is a wall
def isThisWall(stateSequence, direction):
    if direction == 'E':
        if maze[stateSequence - 1 + 1].isWall == False:
            return (stateSequence + 1, 'E')
    elif direction == 'W':
        if maze[stateSequence - 1 - 1].isWall == False:
            return (stateSequence - 1, 'W')
    elif direction == 'N':
        if maze[stateSequence - 1 + COLUMN].isWall == False:
            return (stateSequence + COLUMN, 'N')
    elif direction == 'S':
        if maze[stateSequence - 1 - COLUMN].isWall == False:
            return (stateSequence - COLUMN, 'S')
    return True


# assign available options to each state excluding donut, forbidden and wall states
for state in maze:
    if state.isDonut != True and state.isForbidden != True and state.isWall != True:
        availableActions = []
        # square is at the four corners, having two actions based on their location
        if state.stateSequence in [1, COLUMN, (ROW - 1) * COLUMN + 1, ROW * COLUMN]:
            if state.stateSequence % COLUMN == 1:
                isWallResult = isThisWall(state.stateSequence, 'E')
                # under an action - if the going state is not wall, add this action to availableActions
                # same functionality if similar coding block occurs in this loop
                if type(isWallResult) is tuple:
                    availableActions.append(isWallResult)
                # lower left corner
                if state.stateSequence == 1:
                    isWallResult = isThisWall(state.stateSequence, 'N')
                    if type(isWallResult) is tuple:
                        availableActions.append(isWallResult)
                # upper left corner
                elif state.stateSequence == (ROW - 1) * COLUMN + 1:
                    isWallResult = isThisWall(state.stateSequence, 'S')
                    if type(isWallResult) is tuple:
                        availableActions.append(isWallResult)
            elif state.stateSequence % COLUMN == 0:
                isWallResult = isThisWall(state.stateSequence, 'W')
                if type(isWallResult) is tuple:
                    availableActions.append(isWallResult)
                # lower right corner
                if state.stateSequence == COLUMN:
                    isWallResult = isThisWall(state.stateSequence, 'N')
                    if type(isWallResult) is tuple:
                        availableActions.append(isWallResult)
                # upper right corner
                elif state.stateSequence == ROW * COLUMN:
                    isWallResult = isThisWall(state.stateSequence, 'S')
                    if type(isWallResult) is tuple:
                        availableActions.append(isWallResult)
        # square is along the south edge, excluding the lower left and lower right corners, having three actions - N, E, W
        elif state.stateSequence in range(2, (COLUMN - 1) + 1):
            isWallResult = isThisWall(state.stateSequence, 'N')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'E')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'W')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
        # square is along the north edge, excluding the upper left and lower right corners, having three actions - E, S, W
        elif state.stateSequence in range((ROW - 1) * COLUMN + 1 + 1, (ROW * COLUMN) - 1 + 1):
            isWallResult = isThisWall(state.stateSequence, 'E')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'S')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'W')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
        # square is along the west edge, excluding the upper left and lower left corners, having three actions - N, E, S
        elif state.stateSequence in range(1 * COLUMN + 1, (ROW - 2) * COLUMN + 1 + 1, COLUMN):
            isWallResult = isThisWall(state.stateSequence, 'N')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'E')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'S')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
        # square is along the east edge, excluding the upper right and lower right corners, having three actions - N, S, W
        elif state.stateSequence in range(2 * COLUMN, (ROW - 1) * COLUMN + 1, COLUMN):
            isWallResult = isThisWall(state.stateSequence, 'N')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'S')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'W')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
        # square is not on the edge, having four actions - N, E, S, W
        else:
            isWallResult = isThisWall(state.stateSequence, 'N')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'E')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'S')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
            isWallResult = isThisWall(state.stateSequence, 'W')
            if type(isWallResult) is tuple:
                availableActions.append(isWallResult)
        # give the available actions to the state
        state.availableActions = availableActions

# debug - print the initial maze
# for state in maze:
#     print(state)

# based on the Q-values of the current state, calculate the best action
# if epsilon falls into the probability then a random action is chosen
def bestAction(availableActions, qValues, epsilon):
    # qValues = [N, E, S, W]
    actionWithQVals = []
    for actionItem in availableActions:
        if actionItem[1] == 'N':
            actionWithQVals.append(['N', qValues[0]])
        elif actionItem[1] == 'E':
            actionWithQVals.append(['E', qValues[1]])
        elif actionItem[1] == 'S':
            actionWithQVals.append(['S', qValues[2]])
        else:
            actionWithQVals.append(['W', qValues[3]])
    action, qVal = max(actionWithQVals, key=lambda item: item[1])
    if epsilon == 0:
        return action
    else:
        probability = random.uniform(0, 1)
        if probability <= epsilon:
            return (random.choice(actionWithQVals)[0])
        else:
            return action

# the function updates the Q-values for the current state and
# return the going state based on the action received from bestAction()
def updateQValAndReturnGoToState(state, action):
    for actionItem in state.availableActions:
        if actionItem[1] == action:
            goToState = actionItem[0]
    goToStateMaxQVal = max(maze[goToState - 1].qValues)
    if action == 'N':
        qValueIndex = 0
    elif action == 'E':
        qValueIndex = 1
    elif action == 'S':
        qValueIndex = 2
    elif action == 'W':
        qValueIndex = 3
    state.qValues[qValueIndex] = (1 - LEARNING_RATE) * state.qValues[qValueIndex] + LEARNING_RATE * (
                LIVING_REWARD + DISCOUNT_RATE * goToStateMaxQVal)
    return goToState

# update the value of the exit states - donut and forbidden
def updateValExitStates(state):
    if state.isDonut == True:
        exitReward = DONUT_REWARD
    elif state.isForbidden == True:
        exitReward = FORBIDDEN_REWARD
    state.qValues[0] = (1 - LEARNING_RATE) * state.qValues[0] + LEARNING_RATE * (exitReward)


# start Q learning
i = 0
sequence = START_STATE
while i < ITERATIONS:
    state = maze[sequence - 1]
    while state.isDonut != True and state.isForbidden != True:
        # not the exit state, update Q values and go to the next state
        if i < EPSILON_CONVERGENCE:
            epsilon = EPSILON * (1 - i / EPSILON_CONVERGENCE)
        else:
            epsilon = 0
        action = bestAction(state.availableActions, state.qValues, epsilon)
        sequence = updateQValAndReturnGoToState(state, action)
        state = maze[sequence - 1]
    # reach exit state, update value and restart if iteration is still on going
    updateValExitStates(state)
    sequence = START_STATE
    i += 1

# OUTPUT1 - print the optimal policy
def printPolicy():
    print("Q-values after", ITERATIONS, "iterations:\n")
    for state in maze:
        if state.isDonut == False and state.isForbidden == False and state.isWall == False:
            availableActions = []
            for actionItem in state.availableActions:
                if actionItem[1] == 'N':
                    availableActions.append(['↑', state.qValues[0]])
                elif actionItem[1] == 'E':
                    availableActions.append(['→', state.qValues[1]])
                elif actionItem[1] == 'S':
                    availableActions.append(['↓', state.qValues[2]])
                elif actionItem[1] == 'W':
                    availableActions.append(['←', state.qValues[3]])
            action, qVal = max(availableActions, key=lambda item: item[1])
            print(state.stateSequence, ' ', action)

# OUTPUT2 - print the Q-values of the designated state
def printQVals(stateSequence):
    print("Q-values after", ITERATIONS, "iterations:\n")
    print("State", stateSequence, "has optimal Q-values:")
    print('↑ ', maze[stateSequence - 1].qValues[0])
    print('→ ', maze[stateSequence - 1].qValues[1])
    print('↓ ', maze[stateSequence - 1].qValues[2])
    print('← ', maze[stateSequence - 1].qValues[3])


# output based on the input arguments
if len(arguments) == 5:
    printPolicy()
else:
    stateSequence = int(arguments[5])
    printQVals(stateSequence)
