import pygame
from Agent import Agent
from qtable import save_q_table, load_q_table
from Environment import Environment
from Interpreter import Interpreter
from graphics import draw_apples, draw_board, draw_snake


def run_snake(sessions, explore, model_input, model_output, step, display):
    """set up graphics if appropriate,
    initialize environment, agent, and interpretor,
    run loop of sessions"""

    # set sizes of rewards and penalties
    GREEN_REWARD = 10
    BLANK_REWARD = -1
    DEATH_PENALTY = -20
    RED_PENALTY = -10

    # set sizes of board
    X_SIZE = 20
    Y_SIZE = 20
    aspect = X_SIZE / Y_SIZE
    # board must exceed 6 in size
    if X_SIZE * Y_SIZE < 6:
        print('board size is insufficient')
        exit()
    # board must exceed 1 in width/height
    if X_SIZE < 2 or Y_SIZE < 2:
        print('board too narrow')
        exit()

    # restart length of snake
    LENGTH = 3

    # initialize environment
    environment = Environment(
        X_SIZE, Y_SIZE,
        BLANK_REWARD, DEATH_PENALTY, GREEN_REWARD, RED_PENALTY,
        LENGTH)

    # initialize agent
    agent = Agent(explore)

    # initialize interpreter
    interpreter = Interpreter(min(X_SIZE, Y_SIZE))

    # load previous q-table if available
    q_table = load_q_table(model_input)
    if q_table:
        agent.q_table = q_table

    # initalize state
    state = set_snake(environment, agent, interpreter)

    # print initial q_table
    print(agent.q_table)

    # initialize stat trackers
    max_length = LENGTH
    deaths = 0
    max_steps = 0
    steps = 0

    if display == 'on':
        # Initialize the game engine
        pygame.init()

        # define apple display colors
        GREEN = [0, 255, 0]
        RED = [255, 0, 0]

        # Set the height and width of the screen
        SCREEN_Y = 500
        SCREEN_X = SCREEN_Y * aspect
        SCREEN_SIZE = [SCREEN_X, SCREEN_Y]

        # initialize the screen
        screen = pygame.display.set_mode(SCREEN_SIZE)

        # set up clock for animation
        clock = pygame.time.Clock()

    # Loop until the user clicks the close button or sessions clomplete.
    done = False
    while not done:

        if display == 'on':
            # draw screen elements
            draw_board(screen, X_SIZE, Y_SIZE)
            draw_apples(screen, environment, GREEN, RED, X_SIZE, Y_SIZE)
            draw_snake(screen, environment, X_SIZE, Y_SIZE)

            # update the screen
            pygame.display.flip()

            for event in pygame.event.get():   # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True   # Flag that we are done to exit loop
                if event.type == pygame.KEYDOWN:
                    # step-by-step display, snake is alive
                    if event.key == pygame.K_RETURN:  # if user clicked return
                        # move snake
                        if step == 'on' and environment.snake.alive:
                            steps += 1
                            state = move_snake(
                                state,
                                environment,
                                agent,
                                interpreter,
                                explore)
                        # display vision and snake direction
                        interpreter.print_view()
                        interpreter.print_dir(environment.snake.direction)
                        # note statistics
                        max_length = max(environment.snake.length, max_length)
                        max_steps = max(steps, max_steps)
                    # terminate session prematurely
                    if event.key == pygame.K_TAB:  # if user clicked tab
                        # kill snake
                        environment.snake.alive = False

        # continuous display, snake is alive
        if step == 'off' and environment.snake.alive:
            # pause between steps for visualization
            if display == 'on':
                clock.tick(20)
            steps += 1
            # move snake
            state = move_snake(state, environment, agent, interpreter, explore)
            # note statistics
            max_length = max(environment.snake.length, max_length)
            max_steps = max(steps, max_steps)

        # snake is dead, reset
        if not environment.snake.alive:
            # report statistics for dead snake
            deaths += 1
            print('steps =', steps, 'length', environment.snake.length)
            print('sessions', deaths)
            steps = 0
            # reset snake
            state = set_snake(environment, agent, interpreter)
            # longer pause for visualization
            if display == 'on':
                clock.tick(10)
            # periodic save of progress in case something goes wrong in long run
            if explore == 'yes' and (deaths + 1) % 100 == 0:
                save_q_table(agent.q_table, filename=model_output)

        if deaths == sessions:
            done = True   # Flag that we are done to exit loop

    if explore == 'yes':
        save_q_table(agent.q_table, filename=model_output)
    print('Game over, max_length =', max_length, ', max duration =', max_steps)


def move_snake(state, environment, agent, interpreter, explore):
    """move the snake based on the state and q-table,
    update q-table if in explore mode"""
    # save old state for use in update of q-table
    old_state = state
    # agent - choose action
    action = agent.choose_action(state)
    # environment - move snake
    reward = environment.move_snake(action)
    # get new view and state
    view, direction = environment.get_snake_view()
    # interpreter - get new state
    state = interpreter.get_state(view, direction)
    # update table as appropriate
    if explore:
        new_state = state
        agent.update_table(
            environment.snake.alive,
            action,
            old_state,
            new_state,
            reward)
    return state


def set_snake(environment, agent, interpreter):
    """set/reset snake in environment"""
    # initialize snake
    environment.snake.generate_snake()
    # put out a new set of apples
    environment.apples = []
    environment.initialize_apple_list()
    # environment - get snake view and direction
    view, direction = environment.get_snake_view()
    # interpreter - get state
    state = interpreter.get_state(view, direction)
    # check if state exists in q_table
    agent.check_table(state)
    return state
