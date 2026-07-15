from tools import get_random_step
from Snake import Snake, eat_apple


class Agent:
    """snake class"""
    def __init__(self, board):

        self.board = board
        self.snake = Snake(board)

    def move_snake_random(self, apples):
        """Test code for moving snake"""
        if self.snake.length > 0:
            x, y, bad = self.random_move()
            if bad:
                print("snake is dead")
                self.snake.alive = False
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
