import random


def get_random_action():
    direction = random.randrange(0, 3, 1)
    # print('random direction', direction)
    if direction == 0:
        return 'left'
    elif direction == 1:
        return 'forward'
    else:
        return 'right'


def get_step(x, y, orientation, action):
    if action == 'forward':
        dir = orientation
    elif action == 'right':
        dir = (orientation + 1) % 4
    else:
        dir = (orientation - 1 + 4) % 4

    if dir == 0:
        x -= 1
    elif dir == 1:
        y -= 1
    elif dir == 2:
        x += 1
    else:
        y += 1
    return x, y


def get_action(dir, orientation):
    if dir == orientation:
        return 'forward'
    elif dir == (orientation + 1) % 4:
        return 'right'
    elif dir == (orientation - 1 + 4) % 4:
        return 'left'
    else:
        return 'error'


def get_movement_direction(x1, y1, x0, y0, orientation):
    # find forward direction
    x_dir = x1 - x0
    y_dir = y1 - y0
    if x_dir == 0:
        if y_dir == 1:
            return get_action(3, orientation)
        else:
            return get_action(1, orientation)
    elif y_dir == 0:
        if x_dir == 1:
            return get_action(2, orientation)
        else:
            return get_action(0, orientation)


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
    """check if coords match an apple"""
    for a in apples:
        if a[0] == x and a[1] == y:
            return a[2]
    return 0


def in_wall(board, x, y):
    """check if coords match a wall"""
    if x == -1 or y == -1:
        return True
    if x == board.x_size or y == board.y_size:
        return True
    return False
