import pygame
from Snake import Snake, new_apple
from Board import Board
from Agent import Agent
from qtable import save_q_table, load_q_table


def main():

    explore = False
    max_deaths = 10
    model_name = 'models/q_table.pkl'

    # set sizes of rewards and penalties
    GREEN_REWARD = 10
    BLANK_REWARD = -1
    DEATH_PENALTY = -20
    RED_PENALTY = -10

    # Initialize the game engine
    pygame.init()

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    GREEN = [0, 255, 0]
    BLUE = [135, 206, 235]  # [0, 0, 128]
    RED = [255, 0, 0]

    # set sizes of board
    X_SIZE = 20
    Y_SIZE = 20

    # Set the height and width of the screen
    SCREEN_X = 500
    SCREEN_Y = 500
    SCREEN_SIZE = [SCREEN_X, SCREEN_Y]

    # variables for drawing
    start_x = SCREEN_X / 10
    start_y = SCREEN_Y / 10
    end_x = SCREEN_X - start_x * 2
    end_y = SCREEN_Y - start_y * 2

    screen = pygame.display.set_mode(SCREEN_SIZE)

    # initialize the board with penalty/reward values
    board = Board(X_SIZE, Y_SIZE)

    # initialize agent
    agent = Agent(
        board,
        BLANK_REWARD, DEATH_PENALTY, GREEN_REWARD, RED_PENALTY,
        explore)

    # initialize apples with penalty/reward values
    apples = []
    apples.append(new_apple(agent.snake, apples, 'GREEN'))
    apples.append(new_apple(agent.snake, apples, 'GREEN'))
    apples.append(new_apple(agent.snake, apples, 'RED'))

    # initalize state
    agent.get_state(apples)

    # load previous q-table
    q_table = load_q_table(model_name)
    if q_table:
        agent.q_table = q_table
    print(q_table)

    max_length = agent.snake.length
    deaths = 0
    steps = 0

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

        # draw apples
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # advance time
                    clock.tick(1)

                    agent.print_view()
                    agent.print_direction()
                    # advance time
                    for i in range(3):
                        clock.tick(1)

                    # if agent.snake.alive:
                    #     # move snake
                    #     agent.interpreter(apples)
                    # else:
                    #     # pause
                    #     clock.tick(1)
                    #     # generate new snake
                    #     agent.snake = Snake(board)
                    #     agent.get_state(apples)
                if event.key == pygame.K_TAB:
                    # kill snake
                    agent.snake.alive = False

        clock.tick(20)

        if agent.snake.alive:
            # move snake
            steps += 1
            agent.interpreter(apples)
            max_length = max(agent.snake.length, max_length)
        else:
            # reprot statistics for dead snake
            deaths += 1
            print('steps =', steps, 'length', agent.snake.length)
            print('sessions', deaths)
            steps = 0

            clock.tick(10)
            # generate new snake
            agent.snake = Snake(board)
            agent.get_state(apples)

        if deaths == max_deaths:
            done = True   # Flag that we are done to exit loop

    if explore:
        save_q_table(agent.q_table)
    print('max_length', max_length)


if __name__ == "__main__":
    main()
