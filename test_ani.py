import pygame
from Snake import Snake, new_apple
from Board import Board
from Agent import Agent


def main():

    normal = 1

    # Initialize the game engine
    pygame.init()

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 128]
    RED = [255, 0, 0]

    X_SIZE = 10
    Y_SIZE = 10

    # Set the height and width of the screen
    SCREEN_X = 500
    SCREEN_Y = 500
    SCREEN_SIZE = [SCREEN_X, SCREEN_Y]

    # variables  for drawing
    start_x = SCREEN_X / 10
    start_y = SCREEN_Y / 10
    end_x = SCREEN_X - start_x * 2
    end_y = SCREEN_Y - start_y * 2

    screen = pygame.display.set_mode(SCREEN_SIZE)

    # initialize the board
    board = Board(X_SIZE, Y_SIZE)

    # initialize agent
    agent = Agent(board)

    # initialize apples
    apples = []
    apples.append(new_apple(agent.snake, apples, 'GREEN'))
    apples.append(new_apple(agent.snake, apples, 'GREEN'))
    apples.append(new_apple(agent.snake, apples, 'RED'))

    # initalize state
    agent.snake.get_state(apples)

    # set up clock for animation
    clock = pygame.time.Clock()

    # Loop until the user clicks the close button.
    done = False
    while not done:

        # Set the screen background
        screen.fill(WHITE)

        # draw board
        pygame.draw.rect(screen, BLACK, (start_x, start_y, end_x, end_y))
        for y in range(Y_SIZE + 1):
            pos = start_y + y * end_y / Y_SIZE
            pygame.draw.line(
                screen, WHITE, (start_x, pos), (end_x + start_x, pos), 2)
        for x in range(X_SIZE + 1):
            pos = start_x + x * end_x / X_SIZE
            pygame.draw.line(
                screen, WHITE, (pos, start_y), (pos, end_y + start_y), 2)

        # place apples
        for apple in apples:
            x = start_x + apple[0] * end_x / X_SIZE + 2
            y = start_y + apple[1] * end_y / Y_SIZE + 2
            pygame.draw.rect(
                screen, apple[2],
                (x, y,  end_x / X_SIZE - 2, end_y / Y_SIZE - 2))

        # draw snake
        for s in range(agent.snake.length):
            x = start_x + agent.snake.body[s][0] * end_x / X_SIZE + 2
            y = start_y + agent.snake.body[s][1] * end_y / Y_SIZE + 2
            pygame.draw.rect(
                screen, BLUE, (x, y, end_x / X_SIZE - 2, end_y / Y_SIZE - 2))
            if s == agent.snake.length - 1:
                pygame.draw.circle(
                    screen, WHITE,
                    (x + end_x / X_SIZE / 2, y + end_y / Y_SIZE / 2), 2, 0)

        # update the screen
        pygame.display.flip()

        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done to exit loop
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:

            #         # advance time
            #         clock.tick(1)
            #         # clock.tick(3)

            #         if agent.snake.alive:
            #             # move snake
            #             agent.move_snake(apples)
            #             agent.snake.get_state(apples)
            #         else:
            #             # pause
            #             clock.tick(1)
            #             # generate new snake
            #             agent.snake = Snake(board)
            #             agent.snake.get_state(apples)


        clock.tick(3)
        # clock.tick(3)

        if agent.snake.alive:
            # move snake
            agent.move_snake(apples)
            agent.snake.get_state(apples)
        else:
            # pause
            clock.tick(1)
            # generate new snake
            agent.snake = Snake(board)
            agent.snake.get_state(apples)

if __name__ == "__main__":
    main()
