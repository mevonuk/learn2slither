from tools import get_random_step, in_apple


class Snake:
    """snake class"""
    def __init__(self, board, length=3):

        self.length = length
        self.alive = True
        self.board = board
        self.generate_snake()

    def generate_snake(self):
        self.body = []
        x, y = self.board.get_random_coords()
        self.body.append((x, y))
        for i in range(self.length - 1):
            good = False
            while not good:
                x, y, bad = self.random_move()
                if not bad:
                    self.body.append((x, y))
                    good = True

    def move_snake(self, apples):
        """Test code for moving snake"""
        if self.length > 0:
            x, y, bad = self.random_move()
            if bad:
                print("snake is dead")
                self.alive = False
            self.body.append((x, y))
            pop_it = True
            for a in range(len(apples)):
                if (
                    apples[a][0] == self.body[-1][0]
                    and apples[a][1] == self.body[-1][1]
                ):
                    pop_it = eat_apple(self, apples, a)
                    break
            if pop_it:
                self.pop_snake()
        if self.length == 0:
            print("snake has zero length")
            print("snake is dead")
            self.alive = False

    def random_move(self):
        """choose a random step for snake:
        forward, left, or right"""
        bad = False
        if len(self.body) > 1:
            last_move = self.body[-2]
        else:
            last_move = self.body[-1]
        x, y = get_random_step(last_move, self.body[-1])
        # check if coordinate is already occupied by snake and on board
        if self.in_snake(x, y):
            print("snake ate its tail")
            bad = True
        if not self.board.on_board(x, y):
            print("snake hit the wall")
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
        if not in_apple(apples, x, y) and not snake.in_snake(x, y):
            found = True

    return (x, y, color)


def eat_apple(snake, apples, a):
    """snake eats apple,
    faces concequences,
    and a new apple is generated"""
    pop_it = True
    if apples[a][2] == 'RED':
        # shrink snake
        snake.pop_snake()
        b = new_apple(snake, apples, 'RED')
    else:
        # don't pop the snake, let it grow
        pop_it = False
        b = new_apple(snake, apples, 'GREEN')
    # remove eaten apple
    apples.pop(a)
    # add new apple
    apples.append(b)
    return pop_it
