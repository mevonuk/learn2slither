# learn2slither

## Description

A project about reinforcement learning (Q-learning). A snake agent learns to survive on a board whilst eating apples to change its length and avoiding hitting walls and itself.

*This project has been created as part of the 42 curriculum.*

### Contributor
- M. Evonuk (https://github.com/mevonuk)

## Tools
- Coding Language: Python

## Project overview

### Board

A board is created with a default size of 10 x 10. The board contains a randomly placed red apple and two randomly placed green apples. A snake of length 3 units is randomly placed on the board.

### Goal of the snake

The snake (blue) seeks to have a length of 10 or more and to last as long as possible without dying. This goal is not explicitly given to the snake, but is encouraged by the rewards and penalties.

### Rules

- If the snake hits a wall, it dies.
- If the snake collides with its own tail, it dies.
- If the snake eats a green apple, it's length increases by 1 and a new green apple appears randomly on the board.
- If the snake eats a red apple, it's length decreases by 1 and a new red apple appears randomly on the board.
- If the snake's length decreases to 0, the snake dies.

### Modular design

For testing purposes the program has the following modules:
- Environment
    - Board
    - Apples
    - Snake
- Interpreter
- Agent

## Environment

The environment consists of the board, the apples, and the snake. It receives an action from the agent which it then executes by moving the snake. The movement of the snake results in a reward (based on hitting the wall or tail, eating an apple, or entering an empty space). The snake's view and the reward following the step are passed to the interpreter and then the agent.

### Board

The board is 2D and can be square or rectangular. Methods include generating a random coordinate set within the board and checking if a set of coordinates is on the board.

### Apples

A list of three apples (two green and one red) is maintained in the environment. Apples can be eaten by the snake; if so, they are replaced at random coordinates to maintain a constant number of apples.

### Snake

The snake starts with three segments, randomly located on the board. The snake can see in the four board directions from its head. This is its view. The view is passed to the interpreter to create a state, which is then given to the agent.

If the snake dies, the snake is reset to the default length at a random spot on the board.

## Interpreter

The interpreter converts the snake view into a state for the agent. In addition, in the step-by-step mode, the interpreter prints the snake's view to the console as well as the direction on the board that the snake last stepped.

### State

The interpreter creates a state by determining the nearest object in three views: forward; left; and right. The state objects are green apple, red apple, wall, and tail. The distance classes to the object are adjacent, near, mid, and far. This greatly reduces the total possible number of states. However, note that, in order to learn not to eat its own tail, the training must run long enough for the snake to have grown to sufficient lengths to have seen its own tail in the various action directions and at the various distances.

The distance to the object can be normalized to allow the model to be used on different size boards than it was trained on.

$d_{norm}$ = distance / total_grid_size

$d_{norm}$ is then sorted into (adjacent, near, mid, far)

state = (
- (distance to nearest object, object) left
- (distance to nearest object, object) forward
- (distance to nearest object, object) right
)

## Agent

The agent receives the state from the interpreter and the reward passed from the environment following a movement.

The snake can see all the way to the wall but only in 4 directions with respect to its head, north, south, east, and west. The interpreter converts this to a state. The agent must decide on the next action based only on this information (and the corresponding information saved in the q-table).

The actions the snake can take are to step forward, step left, or step right. The snake cannot step backwards because this will result in death (except in the case of zero length; however, this case is not treated).

Actions chosen by the agent will evolve through time based on positive and negative rewards and subsequent updates to the q-table. For example:
- eating a green apple = positive reward
- eating a red apple = negative reward
- eating nothing = small negative reward
- dying (hitting the wall or itself or shrinking to length zero) = large negative reward

### Q-learning

A model is implemented to use a Q-function to evaluate the quality of an action in a given state. The Q-learning algorithm adjusts the Q-function based on the reward after each action during the training session.

That is, the agent builds a Q-table that stores Q-values. Q-values provide an estimate of how good it is to take an action given the state and the expectation of future rewards. The Q-table is updated based on feedback (rewards). The agent updates the Q-values using the temporal difference (TD)-update formula:
- $Q(S,A) = Q(S,A) + \alpha (R + \gamma Q(S', A') - Q(S,A)) $

Here,
- $S$ is the current state
- $A$ is the action taken by the agent
- $S'$ is the next state moved to by performing the action
- $A'$ is the projected next best action when in state $S'$
- $R$ is the reward for taking action $A$ in state $S$
- $\gamma$ is the discount factor or the importance of future rewards
- $\alpha$ is the learning rate or how much new information affect the old Q-values

### Q-table

The Q-table contains the q-values for each state and action:

q-table = {
    $state_i$ : {'left': $q_l$, 'forward': $q_f$, 'right': $q_r$}
}

### Training versus exploitation

To balance between exploration and exploitation, the epsilon-greedy policy is used. With probability $1-\epsilon$, the agent picks the action with the highest Q-value, exploiting the information in the Q-table, using current knowledge to maximize the rewards. With probability $\epsilon$, the agent chooses a random action to explore new possibilities.

Learned models can be imported and exported and are independent of board size.

Learning can be disabled to allow the model to be tested.

## Program options

The main program (slither_main.py) can be run with various display and training options.

Options
- sessions : number of snake deaths to run before program terminates
- explore
    - yes : (default) includes random exploration of the action space
    - no : pure exploitation of the q-table
- display
    - on : (default) shows the board, apples, snake, and the snake's movement during the session
    - off : runs the program without a graphics display
- step
    - on : runs the program step-by-step to observe the snake's movement action by action. Prints the snake's view to the console, as well as the direction that the step was taken in. Requires that display='on'
    - off : (default) display is continuous
- load : name of the model (q-table) to be loaded
- save : filename to which to save generated q-table

Additional commands in display mode:
- pressing the RETURN key advances the step-by-step run
- pressing the TAB key kills the snake and initializes a new snake instance
- closing the display window terminates the program saving the latest q-table to the save filename

## To run

To set up virtual environment run:
- make setup

Then, activate the virtual environment.

Default make options include:
- train (trains model from scratch for 100 sessions with continuous display and exploration, saves to models/q_table.pkl)
- evaluate (runs models/q_table10000.pkl for 10 sessions with continuous display and pure exploitation)
- stepit (runs models/q_table10000.pkl for 1 session with step-by-step display and pure exploitation)

The program can also be run with various custom options as indicated in
- make help

When you are finished, deactivate the virtual environment and run:
- make clean

This is will remove the virtual environment and pycache files.
