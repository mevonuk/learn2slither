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

A board is created with a default size of 10x10. The board contains a randomly placed red apple and two randomly placed green apples. A snake of length 3 units is randomly placed on the board.

### Goal of the snake

The snake (blue) seeks to have a length of 10 or more and to last as long as possible without dying.

### Rules

- If the snake hits a wall, it dies.
- If the snake collides with its own tail, it dies.
- If the snake eats a green apple, it's length increases by 1 and a new green apple appears randomly on the board.
- If the snake eats a red apple, it's length decreases by 1 and a new red apple appears randomly on the board.
- If the snake's length decreases to 0, the snake dies.

### Snake agent

The snake can see all the way to the wall but only in 4 directions with respect to it's head, north, south, east, and west. It must decide on it's next move based only on this information.

The actions the snake can take are to step forward, step left, or step right. The snake cannot step backwards because this will result in death.

Actions chosen by the agent will evolve through time based on positive and negative rewards. For example:
- eating a green apple = positive reward
- eating a red apple = negative reward
- eating nothing = small negative reward
- dying (hitting the wall or itself or shrinking to lenght zero) = large negative reward

### Q-learning

A model is implemented to use a Q function to evalute the quality of an action in a given state. The Q-learning algorithm adjusts the Q function based on the reward after each action during the training session.

That is, the agent builds a Q-table that stores Q-values. Q-values provide an estimate of how good it is to take an action given the state and the expectation of future rewards. The Q-table is updated based on feedback (rewards). The agent updates the Q-values using the temporal difference (TD)-update formula:
- $Q(S,A) = Q(S,A) + \alpha (R + \gamma Q(S', A') - Q(S,A)) $

Here,
- $S$ is the current state
- $A$ is the action taken by the agent
- $S'$ is the next state moved to by performing the action
- $A'$ is the project next best action when in state $S'$
- $R$ is the reward for taking action $A$ in state $S$
- $\gamma$ is the discount factor or the importance of future rewards
- $\alpha$ is the learning rate or how much new information affect the old Q-values

To balance between exploration and exploitation, the $\epsilon$-greedy policy is used. With probability $1-\epsilon$, the agent picks the action with the highest Q-value, exploiting the information in the Q-table, using current knowledge to maximize the rewards. With probability $\epsilon$, the agent chooses a random action to explore new possibilities.

Learned models can be imported and exported and should be independent of board size.

Learning can be disabled to allow the model to be tested.

### Modular design

For testng perposes the program has the following modules:
- Environment
- Interpreter
- Agent


## Current

Wrote a dumby code to move snake looking for apples and wall given the state (its vision in the four directions)

Need to now set up Q-learning to make its own rules instead of mine.

Have commented out a code to step through with return key, this should be an option.
