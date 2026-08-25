import pygame


def draw_board(screen, X_SIZE, Y_SIZE):

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]

    SCREEN_X, SCREEN_Y = screen.get_size()

    # variables for drawing
    start_x = 10
    start_y = 10
    end_x = SCREEN_X - start_x * 2
    end_y = SCREEN_Y - start_y * 2

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


def draw_apples(screen, environment, GREEN, RED, X_SIZE, Y_SIZE):

    SCREEN_X, SCREEN_Y = screen.get_size()

    # variables for drawing
    start_x = 10
    start_y = 10
    end_x = SCREEN_X - start_x * 2
    end_y = SCREEN_Y - start_y * 2

    # draw apples
    for apple in environment.apples:
        x = start_x + apple[0] * end_x / X_SIZE + 2
        y = start_y + apple[1] * end_y / Y_SIZE + 2
        pygame.draw.rect(
            screen, apple[2],
            (x, y,  end_x / X_SIZE - 2, end_y / Y_SIZE - 2))


def draw_snake(screen, environment, X_SIZE, Y_SIZE):

    WHITE = [255, 255, 255]
    BLUE = [135, 206, 235]  # [0, 0, 128]

    SCREEN_X, SCREEN_Y = screen.get_size()

    # variables for drawing
    start_x = 10
    start_y = 10
    end_x = SCREEN_X - start_x * 2
    end_y = SCREEN_Y - start_y * 2

    # draw snake
    for s in range(environment.snake.length):
        x = start_x + environment.snake.body[s][0] * end_x / X_SIZE + 2
        y = start_y + environment.snake.body[s][1] * end_y / Y_SIZE + 2
        pygame.draw.rect(
            screen, BLUE, (x, y, end_x / X_SIZE - 2, end_y / Y_SIZE - 2))
        if s == environment.snake.length - 1:
            pygame.draw.circle(
                screen, WHITE,
                (x + end_x / X_SIZE / 2, y + end_y / Y_SIZE / 2), 2, 0)
