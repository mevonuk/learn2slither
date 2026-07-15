from tools import get_random_step
from Snake import Snake, eat_apple
import random


class Agent:
    """snake class"""
    def __init__(self, board):

        self.board = board
        self.snake = Snake(board)

    def step_snake(self, apples, x, y):
        self.snake.body.append((x, y))
        pop_it = True
        for a in range(len(apples)):
            if (
                apples[a][0] == self.snake.body[-1][0]
                and apples[a][1] == self.snake.body[-1][1]
            ):
                pop_it = eat_apple(self.snake, apples, a)
                break
        if pop_it:
            self.snake.pop_snake()

    def move_snake(self, apples):
        # check state for apples
        step, dir = see_apple(self.snake.state)
        x, y = self.snake.body[-1]
        if step == 0:
            step_dir = see_wall(self.snake.state)
            if len(step_dir):
                rand_dir = random.randrange(0, len(step_dir), 1)
                dir = step_dir[rand_dir]
            else:
                dir = random.randrange(0, 4, 1)
        if dir == 0:
            x -= 1
        elif dir == 1:
            y -= 1
        elif dir == 2:
            x += 1
        else:
            y += 1
        if self.snake.in_snake(x, y):
            print("snake is dead")
            self.snake.alive = False
        self.step_snake(apples, x, y)

    def move_snake_random(self, apples):
        """Test code for moving snake"""
        self.snake.previous = self.snake.body[-1]
        if self.snake.length > 0:
            x, y, bad = self.random_move()
            if bad:
                print("snake is dead")
                self.snake.alive = False
            self.step_snake(apples, x, y)
        if self.snake.length == 0:
            print("snake has zero length")
            print("snake is dead")
            self.snake.alive = False

    def move_snake_safe(self, apples):
        """Test code for moving snake"""
        if self.snake.length > 0:
            safe = False
            patience = 10
            counter = 0
            while not safe:
                counter += 1
                x, y, bad = self.random_move()
                if not bad:
                    safe = True
                if counter > patience:
                    self.snake.alive = False
                    print("snake stuck")
                    break
            self.snake.body.append((x, y))
            pop_it = True
            for a in range(len(apples)):
                if (
                    apples[a][0] == self.snake.body[-1][0]
                    and apples[a][1] == self.snake.body[-1][1]
                ):
                    pop_it = eat_apple(self.snake, apples, a)
                    break
            if pop_it:
                self.snake.pop_snake()
        if self.snake.length == 0:
            print("snake has zero length")
            print("snake is dead")
            self.snake.alive = False

    # def apple_check(self, apples):

    def random_move(self):
        """choose a random step for snake:
        forward, left, or right"""
        bad = False
        if len(self.snake.body) > 1:
            last_move = self.snake.body[-2]
        else:
            last_move = self.snake.body[-1]
        x, y = get_random_step(last_move, self.snake.body[-1])
        # check if coordinate is already occupied by snake and on board
        if self.snake.in_snake(x, y):
            print("snake ate its tail")
            bad = True
        if not self.board.on_board(x, y):
            print("snake hit the wall")
            bad = True
        return x, y, bad


def see_apple(state):
    dist = 0
    for s in range(len(state)):
        if state[s][0] not in ['S', 'W']:
            for a in range(len(state[s])):
                if state[s][a] in ['G']:
                    return a + 1, s
    return dist, 0


def see_wall(state):
    dir = []
    for s in range(len(state)):
        if state[s][0] not in ['S', 'W']:
            dir.append(s)
    return dir
