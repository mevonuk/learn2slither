import random


class Snake:
    """snake class"""
    def __init__(self, board, length=3):

        self.base_length = length
        self.board = board
        self.generate_snake()

    def get_direction(self):
        """find forward moving direction of snake"""
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
        """randomly initialize a snake of default length"""
        self.alive = True
        self.body = []
        self.length = self.base_length
        x, y = self.board.get_random_coords()
        self.body.append((x, y))
        for i in range(self.length - 1):
            good = False
            patience = 0
            while not good and patience < 10:
                patience += 1
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


def get_random_step(last_move, s):
    """generate a random step from s"""
    found = False
    while not found:
        direction = random.randrange(0, 4, 1)
        x = s[0]
        y = s[1]
        if direction == 0:
            x += 1
        elif direction == 1:
            y += 1
        elif direction == 2:
            x -= 1
        else:
            y -= 1
        if x == last_move[0] and y == last_move[1]:
            found = False
        else:
            found = True
    return x, y
