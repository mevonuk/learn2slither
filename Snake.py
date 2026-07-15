from tools import get_random_step, in_apple, in_wall


class Snake:
    """snake class"""
    def __init__(self, board, length=3):

        self.length = length
        self.alive = True
        self.board = board
        self.generate_snake()
        self.state = []
    
    def get_direction(self):
        # find forward direction
        x_dir = self.body[-1][0] - self.previous[0]
        y_dir = self.body[-1][1] - self.previous[1]
        if x_dir == 0:
            if y_dir == 1:
                self.direction = "s"
            else:
                self.direction = "n"
        elif y_dir == 0:
            if x_dir == 1:
                self.direction = "e"
            else:
                self.direction = "w"


    def get_state(self, apples):
        # find view in four directions from head
        x, y = self.body[-1]
        self.get_direction()
        # horizontal_view = []
        # for i in range(-1, self.board.x_size + 1):
        #     if in_wall(self.board, i, y):
        #         horizontal_view.append('W')
        #     elif i == x:
        #         horizontal_view.append('H')
        #     elif self.in_snake(i, y):
        #         horizontal_view.append('S')
        #     elif in_apple(apples, i, y):
        #         horizontal_view.append(in_apple(apples, i, y)[0])
        #     else:
        #         horizontal_view.append('0')
        # print(horizontal_view)
        # vertical_view = []
        # for i in range(-1, self.board.y_size + 1):
        #     if in_wall(self.board, x, i):
        #         vertical_view.append('W')
        #     elif i == y:
        #         vertical_view.append('H')
        #     elif self.in_snake(x, i):
        #         vertical_view.append('S')
        #     elif in_apple(apples, x, i):
        #         vertical_view.append(in_apple(apples, x, i)[0])
        #     else:
        #         vertical_view.append('0')
        # print(vertical_view)

        view_0 = []
        for i in range(x - 1, -2, -1):
            if in_wall(self.board, i, y):
                view_0.append('W')
            elif self.in_snake(i, y):
                view_0.append('S')
            elif in_apple(apples, i, y):
                view_0.append(in_apple(apples, i, y)[0])
            else:
                view_0.append('0')
        view_1 = []
        for i in range(y - 1, -2, -1):
            if in_wall(self.board, x, i):
                view_1.append('W')
            elif self.in_snake(x, i):
                view_1.append('S')
            elif in_apple(apples, x, i):
                view_1.append(in_apple(apples, x, i)[0])
            else:
                view_1.append('0')
        view_2 = []
        for i in range(x + 1, self.board.x_size + 1):
            if in_wall(self.board, i, y):
                view_2.append('W')
            elif self.in_snake(i, y):
                view_2.append('S')
            elif in_apple(apples, i, y):
                view_2.append(in_apple(apples, i, y)[0])
            else:
                view_2.append('0')
        view_3 = []
        for i in range(y + 1, self.board.y_size + 1):
            if in_wall(self.board, x, i):
                view_3.append('W')
            elif self.in_snake(x, i):
                view_3.append('S')
            elif in_apple(apples, x, i):
                view_3.append(in_apple(apples, x, i)[0])
            else:
                view_3.append('0')

        self.state = [view_0, view_1, view_2, view_3]
        print('state')
        print('west', self.state[0])
        print('north', self.state[1])
        print('east', self.state[2])
        print('south', self.state[3])

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
