from tools import get_random_step, in_apple


class Snake:
    """snake class"""
    def __init__(self, board, length=3):

        self.length = length
        self.alive = True
        self.board = board
        self.generate_snake()

    def get_direction(self):
        # find forward direction
        x_dir = self.head[0] - self.previous[0]
        y_dir = self.head[1] - self.previous[1]
        if x_dir == 0:
            if y_dir == 1:
                return 3  # 3 / down / south
            else:
                return 1  # 1 / up / north
        elif y_dir == 0:
            if x_dir == 1:
                return 2  # 2 / east / right
            else:
                return 0  # 0 / west / left

    def generate_snake(self):
        self.body = []
        x, y = self.board.get_random_coords()
        self.body.append((x, y))
        for i in range(self.length - 1):
            good = False
            while not good:
                x, y, bad = self.random_segment()
                if not bad:
                    self.body.append((x, y))
                    good = True

        self.previous = self.body[-2]
        self.head = self.body[-1]

    def random_segment(self):
        """choose a random step for snake segment:
        forward, left, or right"""
        bad = False
        if len(self.body) > 1:
            last_move = self.body[-2]
        else:
            last_move = self.body[-1]
        x, y = get_random_step(last_move, self.body[-1])
        # check if coordinate is already occupied by snake and on board
        if self.in_snake(x, y):
            bad = True
        if not self.board.on_board(x, y):
            bad = True
        return x, y, bad

    def in_snake(self, x, y):
        """check if coords are in snake"""
        for s in self.body:
            if s[0] == x and s[1] == y:
                return True

    def pop_snake(self):
        """shorten tail of snake"""
        self.body.pop(0)
        self.length = len(self.body)


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
    faces concequences,
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
