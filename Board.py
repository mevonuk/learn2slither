import random


class Board:
    """board class"""
    def __init__(self, x_size=10, y_size=10):

        self.x_size = x_size
        self.y_size = y_size

    def on_board(self, x, y):
        """check if location on board"""
        if x < self.x_size and x > -1:
            if y < self.y_size and y > -1:
                return True
        return False

    def get_random_coords(self):
        """generate random coordinates on the board"""
        x = random.randrange(0, self.x_size, 1)
        y = random.randrange(0, self.y_size, 1)
        return x, y
