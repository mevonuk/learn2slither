from tools import in_apple, in_wall, get_random_action, get_step
from Snake import Snake, eat_apple
import random


class Agent:
    """snake class"""
    def __init__(
            self, board,
            blank_reward=-1,
            death_penalty=-20,
            green_reward=10,
            red_penalty=-5,
            explore=True):

        self.board = board
        self.snake = Snake(board)

        self.death_penalty = death_penalty
        self.blank_reward = blank_reward
        self.green_reward = green_reward
        self.red_penalty = red_penalty

        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.explore = explore

        self.reward = 0
        self.view = []
        self.q_table = {}
        self.last_change = 0

    def step_snake(self, apples, x, y):
        self.snake.body.append((x, y))
        pop_it = True
        for a in range(len(apples)):
            if (
                apples[a][0] == self.snake.body[-1][0]
                and apples[a][1] == self.snake.body[-1][1]
            ):
                pop_it, self.reward = eat_apple(
                    self.snake, apples, a, self.green_reward, self.red_penalty)
                break
        if pop_it:
            self.snake.pop_snake()
        new_length = len(self.snake.body)
        if new_length != self.snake.length:
            self.last_change = 0
        else:
            self.last_change += 1
        self.snake.length = new_length

    def move_snake(self, apples):
        self.reward = self.blank_reward
        epsilon = 0.1
        max_q = max(self.q_table[self.state].values())
        min_q = min(self.q_table[self.state].values())
        if max_q == min_q:
            print('new state', max)
            action = get_random_action()
        elif self.explore and random.random() < epsilon:
            # print('exploring')
            action = get_random_action()
        else:
            # print('from table')
            action = max(
                self.q_table[self.state],
                key=self.q_table[self.state].get
                )
        # get coordinates of a step in the action direction
        x, y = get_step(
            self.snake.head[0],
            self.snake.head[1],
            self.snake.direction,
            action
            )
        # check if coordinate is already occupied by snake and on board
        if self.snake.in_snake(x, y):
            print("snake ate its tail")
            self.snake.alive = False
            self.reward = self.death_penalty
        elif not self.board.on_board(x, y):
            print("snake hit the wall")
            self.snake.alive = False
            self.reward = self.death_penalty
        else:
            self.step_snake(apples, x, y)
        if self.snake.length == 0:
            print("no more snake")
            self.snake.alive = False
            self.reward = self.death_penalty
            return action
        self.snake.previous = self.snake.head
        self.snake.head = self.snake.body[-1]
        return action

    def get_state(self, apples):
        # find view in four directions from head of snake
        x, y = self.snake.head
        self.snake.direction = self.snake.get_direction()

        view_w = []
        for i in range(x - 1, -2, -1):
            if in_wall(self.board, i, y):
                view_w.append('W')
            elif self.snake.in_snake(i, y):
                view_w.append('S')
            elif in_apple(apples, i, y):
                view_w.append(in_apple(apples, i, y)[0])
            else:
                view_w.append('0')
        view_n = []
        for i in range(y - 1, -2, -1):
            if in_wall(self.board, x, i):
                view_n.append('W')
            elif self.snake.in_snake(x, i):
                view_n.append('S')
            elif in_apple(apples, x, i):
                view_n.append(in_apple(apples, x, i)[0])
            else:
                view_n.append('0')
        view_e = []
        for i in range(x + 1, self.board.x_size + 1):
            if in_wall(self.board, i, y):
                view_e.append('W')
            elif self.snake.in_snake(i, y):
                view_e.append('S')
            elif in_apple(apples, i, y):
                view_e.append(in_apple(apples, i, y)[0])
            else:
                view_e.append('0')
        view_s = []
        for i in range(y + 1, self.board.y_size + 1):
            if in_wall(self.board, x, i):
                view_s.append('W')
            elif self.snake.in_snake(x, i):
                view_s.append('S')
            elif in_apple(apples, x, i):
                view_s.append(in_apple(apples, x, i)[0])
            else:
                view_s.append('0')

        view = [view_w, view_n, view_e, view_s]
        self.view = view
        forward = self.snake.direction
        right = (self.snake.direction + 1) % 4
        left = (self.snake.direction - 1)
        view_forward = view[forward]
        view_right = view[right]
        view_left = view[left]
        size = min(self.board.x_size, self.board.y_size)
        self.state = (
            get_nearest_object(view_left, size),
            get_nearest_object(view_forward, size),
            get_nearest_object(view_right, size),
        )
        if self.state not in self.q_table:
            self.q_table[self.state] = {
                "left": 0.0,
                "forward": 0.0,
                "right": 0.0,
            }

    def update_table(self, action, old_state, new_state):
        old_q = self.q_table[old_state][action]
        if not self.snake.alive:
            target = self.reward
        else:
            future_q = max(self.q_table[new_state].values())
            target = self.reward + self.discount_factor * future_q
        self.q_table[old_state][action] = (
            old_q + self.learning_rate * (target - old_q)
        )

    def interpreter(self, apples):
        old_state = self.state
        action = self.move_snake(apples)
        self.get_state(apples)
        if self.explore:
            new_state = self.state
            self.update_table(action, old_state, new_state)

    def print_view(self):
        indent = ''
        for i in range(len(self.view[0])):
            indent += ' '
        for i in range(len(self.view[1]) - 1, -1, -1):
            str = indent + self.view[1][i]
            print(str)
        str = ''
        for i in range(len(self.view[0]) - 1, -1, -1):
            str += self.view[0][i]
        str += 'H'
        for i in range(len(self.view[2])):
            str += self.view[2][i]
        print(str)
        for i in range(len(self.view[3])):
            str = indent + self.view[3][i]
            print(str)
        print()

    def print_direction(self):
        dirs = ['LEFT', 'UP', 'RIGHT', 'DOWN']
        print(dirs[self.snake.direction])
        print()


def get_nearest_object(view, size):
    objects = ['W', 'S', 'R', 'G']
    for i in range(len(view)):
        if view[i] in objects:
            return get_scaled_distance(i, size), get_danger(view[i])


def get_scaled_distance(d, size):
    """returning normalized distance range"""
    d_norm = d / size * 10
    if d_norm == 0:
        return 'adj'
    elif d_norm >= 1 and d_norm <= 3:
        return 'near'
    elif d_norm >= 4 and d_norm <= 6:
        return 'mid'
    else:
        return 'far'


def get_danger(obj):
    """return danger level of object"""
    return obj
    if obj in ['W', 'S']:
        return 'death'
    elif obj == 'G':
        return 'grow'
    elif obj == 'R':
        return 'shrink'
    else:
        return 'live'
