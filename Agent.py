import random


class Agent:
    """agent class"""
    def __init__(self,
                 explore='yes',
                 learning_rate=0.1,
                 discount_factor=0.95,
                 epsilon=0.05):

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        if explore == 'yes':
            self.explore = True
            self.epsilon = epsilon
        else:
            self.explore = False
            self.epsilon = 0
        self.q_table = {}

    def check_table(self, state):
        """check if state is in table,
        if not, add with zero values"""
        if state not in self.q_table:
            self.q_table[state] = {
                "left": 0.0,
                "forward": 0.0,
                "right": 0.0,
            }

    def update_table(self, alive, action, old_state, new_state, reward):
        """update q-table based on states and reward"""
        self.check_table(old_state)
        self.check_table(new_state)
        old_q = self.q_table[old_state][action]
        if not alive:
            target = reward
        else:
            future_q = max(self.q_table[new_state].values())
            target = reward + self.discount_factor * future_q
        self.q_table[old_state][action] = (
            old_q + self.learning_rate * (target - old_q)
        )

    def choose_action(self, state):
        """choose action based on q-table values
        or random action if new state or exploring"""
        self.check_table(state)
        max_q = max(self.q_table[state].values())
        min_q = min(self.q_table[state].values())
        if max_q == min_q:
            print('even state', state)
            action = get_random_action()
        elif self.explore and random.random() < self.epsilon:
            action = get_random_action()
        else:
            action = max(
                self.q_table[state],
                key=self.q_table[state].get
                )
        return action


def get_random_action():
    """pick a random action for snake"""
    direction = random.randrange(0, 3, 1)
    if direction == 0:
        return 'left'
    elif direction == 1:
        return 'forward'
    else:
        return 'right'
