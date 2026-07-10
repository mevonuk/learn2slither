import pygame
import random


def in_snake(snake, x, y):
    """check if coords are in snake"""
    for s in snake:
        if s[0] == x and s[1] == y:
            return True


def in_apple(apples, x, y):
    """check if coords match another apple"""
    for a in apples:
        if a[0] == x and a[1] == y:
            return True


def get_random_coords():
    """generate random coordinates"""
    x = random.randrange(0,9,1)
    y = random.randrange(0,9,1)
    return x, y


def new_apple(snake, apples, color):
    """generate a new apple"""
    found = False
    while not found:
        x, y = get_random_coords()
        # need to check if coordinate is already occupied
        if not in_apple(apples, x, y) and not in_snake(snake, x, y):
            found = True

    return (x,y,color)


def eat_apple(snake, apples, a):
    """snake eats apple,
    faces concequences,
    and a new apple is generated"""
    pop_it = True
    if apples[a][2] == 'RED':
        # shrink snake
        snake.pop(0)
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


def get_random_step(last_move, s):
    """generate a random step from s"""
    found = False
    while not found:
        direction = random.randrange(0,4,1)
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


def on_board(x, y):
    """is the step on the board"""
    if x < 10 and x > -1:
        if y < 10 and y > -1:
            return True
    return False


def random_move(snake):
    """choose a random step for snake:
    forward, left, or right"""
    dead = False
    if len(snake) > 1:
        last_move = snake[-2]
    else:
        last_move = snake[-1]
    x, y = get_random_step(last_move, snake[-1])
    # check if coordinate is already occupied by snake and on board
    if in_snake(snake, x, y):
        print("snake ate its tail")
        dead = True
    if not on_board(x, y):
        print("snake hit the wall")
        dead = True
    return x, y, dead


def move_snake(snake, apples):
    """Test code for moving snake"""
    if len(snake) > 0:
        x, y, dead = random_move(snake)
        snake.append((x, y))
        pop_it = True
        for a in range(len(apples)):
            if apples[a][0] == snake[-1][0] and apples[a][1] == snake[-1][1]:
                pop_it = eat_apple(snake, apples, a)
                break
        if pop_it:
            snake.pop(0)
    if len(snake) == 0:
        print("snake has zero length")
        dead = True
    return dead


def generate_snake():
    snake = []
    x, y = get_random_coords()
    snake.append((x,y))
    for i in range(2):
        good = False
        while not good:
            x, y, bad = random_move(snake)
            if not bad:
                snake.append((x,y))
                good = True
    return snake


def main():

    # Initialize the game engine
    pygame.init()
    
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 128]
    RED = [255, 0, 0]
    
    # Set the height and width of the screen
    SIZE = [500, 500]
    
    screen = pygame.display.set_mode(SIZE)

    # initialize snake
    snake = generate_snake()

    # initialize apples
    apples = []
    apples.append(new_apple(snake, apples, 'GREEN'))
    apples.append(new_apple(snake, apples, 'GREEN'))
    apples.append(new_apple(snake, apples, 'RED'))

    clock = pygame.time.Clock()
    
    # Loop until the user clicks the close button.
    done = False
    while not done:
    
        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done so we exit this loop
    
        # Set the screen background
        screen.fill(WHITE)
    
        # draw board
        pygame.draw.rect(screen, BLACK,
                            (50, 50, 400, 400))
        for x in range(10):
            pos = 50 + x * 40
            pygame.draw.line(screen, WHITE,
                            (pos, 50), (pos, 450), 2)
            pygame.draw.line(screen, WHITE,
                            (50, pos), (450, pos), 2)

        # place apples
        for apple in apples:
            x = 50 + apple[0] * 40 + 2
            y = 50 + apple[1] * 40 + 2
            pygame.draw.rect(screen, apple[2],
                                (x, y, 38, 38))

        # draw snake
        for s in range(len(snake)):
            x = 50 + snake[s][0] * 40 + 2
            y = 50 + snake[s][1] * 40 + 2
            pygame.draw.rect(screen, BLUE,
                                (x, y, 38, 38))
            if s == len(snake) - 1:
                pygame.draw.circle(screen,
                        WHITE, (x + 20, y + 20), 2, 0)
    
        # update the screen
        pygame.display.flip()

        # advance time
        clock.tick(2)

        # move snake
        dead = move_snake(snake, apples)
        if dead:
            print("snake is dead")
            done = True


if __name__ == "__main__":
    main()
