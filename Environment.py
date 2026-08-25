from Board import Board
from Snake import Snake


class Environment:
    def __init__(self, x_size=10, y_size=10,
                 blank_reward=-1,
                 death_penalty=-20,
                 green_reward=10,
                 red_penalty=-5,
                 length=3):

        self.x_size = x_size
        self.y_size = y_size
        self.init_snake_length = length

        self.death_penalty = death_penalty
        self.blank_reward = blank_reward
        self.green_reward = green_reward
        self.red_penalty = red_penalty

        self.board = Board(x_size, y_size)
        self.snake = Snake(self.board, self.init_snake_length)
        self.apples = []
        self.initialize_apple_list()

    def initialize_apple_list(self):
        """initialize three apples"""
        self.apples.append(new_apple(self.snake, self.apples, 'GREEN'))
        self.apples.append(new_apple(self.snake, self.apples, 'GREEN'))
        self.apples.append(new_apple(self.snake, self.apples, 'RED'))

    def get_step_coords(self, action):
        """get coordinates of a step in the action direction"""
        x, y = self.snake.head

        if action == 'forward':
            dir = self.snake.direction
        elif action == 'right':
            dir = (self.snake.direction + 1) % 4
        else:
            dir = (self.snake.direction - 1 + 4) % 4

        if dir == 0:
            x -= 1
        elif dir == 1:
            y -= 1
        elif dir == 2:
            x += 1
        else:
            y += 1
        return x, y

    def step_snake(self, x, y):
        """move the snake to the new coordinate"""
        self.snake.body.append((x, y))
        pop_it = True
        for a in range(len(self.apples)):
            if (
                self.apples[a][0] == self.snake.body[-1][0]
                and self.apples[a][1] == self.snake.body[-1][1]
            ):
                pop_it, self.reward = eat_apple(
                    self.snake,
                    self.apples,
                    a,
                    self.green_reward,
                    self.red_penalty
                    )
                break
        if pop_it:
            self.snake.pop_snake()
        self.snake.length = len(self.snake.body)

    def move_snake(self, action):
        """return reward for proposed step,
        take the step if not automatic death"""
        self.reward = self.blank_reward
        x, y = self.get_step_coords(action)
        # check if new coordinate is already occupied by snake and on board
        if self.snake.in_snake(x, y):
            print("snake ate its tail")
            self.snake.alive = False
            self.reward = self.death_penalty
        elif not self.board.on_board(x, y):
            print("snake hit the wall")
            self.snake.alive = False
            self.reward = self.death_penalty
        else:
            # take step
            self.step_snake(x, y)
        # check if snake has non-zero length
        if self.snake.length == 0:
            print("no more snake")
            self.snake.alive = False
            self.reward = self.death_penalty
            return self.reward
        # update coordinates of snake head
        self.snake.previous = self.snake.head
        self.snake.head = self.snake.body[-1]
        return self.reward

    def get_snake_view(self):
        """find view in four directions from head of snake"""
        x, y = self.snake.head

        view_w = []
        for i in range(x - 1, -2, -1):
            if not self.board.on_board(i, y):
                view_w.append('W')
            elif self.snake.in_snake(i, y):
                view_w.append('S')
            elif in_apple(self.apples, i, y):
                view_w.append(in_apple(self.apples, i, y)[0])
            else:
                view_w.append('0')
        view_n = []
        for i in range(y - 1, -2, -1):
            if not self.board.on_board(x, i):
                view_n.append('W')
            elif self.snake.in_snake(x, i):
                view_n.append('S')
            elif in_apple(self.apples, x, i):
                view_n.append(in_apple(self.apples, x, i)[0])
            else:
                view_n.append('0')
        view_e = []
        for i in range(x + 1, self.board.x_size + 1):
            if not self.board.on_board(i, y):
                view_e.append('W')
            elif self.snake.in_snake(i, y):
                view_e.append('S')
            elif in_apple(self.apples, i, y):
                view_e.append(in_apple(self.apples, i, y)[0])
            else:
                view_e.append('0')
        view_s = []
        for i in range(y + 1, self.board.y_size + 1):
            if not self.board.on_board(x, i):
                view_s.append('W')
            elif self.snake.in_snake(x, i):
                view_s.append('S')
            elif in_apple(self.apples, x, i):
                view_s.append(in_apple(self.apples, x, i)[0])
            else:
                view_s.append('0')

        self.view = [view_w, view_n, view_e, view_s]
        self.snake.direction = self.snake.get_direction()
        return self.view, self.snake.direction


def new_apple(snake, apples, color):
    """generate a new apple"""
    found = False
    while not found:
        x, y = snake.board.get_random_coords()
        # need to check if coordinate is already occupied
        if in_apple(apples, x, y) == 0 and not snake.in_snake(x, y):
            found = True

    return (x, y, color)


def eat_apple(snake, apples, a, green_reward, red_penalty):
    """snake eats apple,
    faces concequences (indicator to change length, reward),
    and a new apple is generated"""
    pop_it = True
    if apples[a][2] == 'RED':
        # shrink snake
        snake.pop_snake()
        b = new_apple(snake, apples, 'RED')
        reward = red_penalty
    else:
        # don't pop the snake, let it grow
        pop_it = False
        b = new_apple(snake, apples, 'GREEN')
        reward = green_reward
    # remove eaten apple
    apples.pop(a)
    # add new apple
    apples.append(b)
    return pop_it, reward


def in_apple(apples, x, y):
    """check if coords match an apple"""
    for a in apples:
        if a[0] == x and a[1] == y:
            return a[2]
    return 0
