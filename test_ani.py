import pygame
import random
 
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
snake = []
snake.append((0,0))
snake.append((0,1))
snake.append((0,2))

# initialize apples
apples = []
apples.append((1,1,'GREEN'))
apples.append((0,5,'GREEN'))
apples.append((7,9,'RED'))

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
    if len(snake) > 0:
        if snake[-1][1] < 9:
            snake.append((snake[-1][0],snake[-1][1] + 1))
        elif snake[-1][0] < 9:
            snake.append((snake[-1][0] + 1,snake[-1][1]))
        no_pop = 0
        for a in range(len(apples)):
            if apples[a][0] == snake[-1][0] and apples[a][1] == snake[-1][1]:
                if apples[a][2] == 'RED':
                    snake.pop(0)
                    apples.pop(a)
                    break
                elif apples[a][2] == 'GREEN':
                    no_pop = 1
                    apples.pop(a)
                    break
        if no_pop == 0:
            snake.pop(0)