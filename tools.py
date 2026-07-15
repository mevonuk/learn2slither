import random


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


def in_apple(apples, x, y):
    """check if coords match another apple"""
    for a in apples:
        if a[0] == x and a[1] == y:
            return True
