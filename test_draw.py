# import pygame module in this program
import pygame

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value
# for white, green,
# blue, black, red
# colour respectively.
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)

# assigning values to X and Y variable
X = 500
Y = 500

# create the display surface object
# of specific dimension..e(X,Y).
display_surface = pygame.display.set_mode((X, Y ))

# set the pygame window name
pygame.display.set_caption('Drawing')

# completely fill the surface object 
# with white colour 
display_surface.fill(white)

# draw a polygon using draw.polygon()
# method of pygame.
# pygame.draw.polygon(surface, color, pointlist, thickness)
# thickness of line parameter is optional.
# pygame.draw.polygon(display_surface, blue,
#                     [(146, 0), (291, 106), (1,1),
#                     (236, 277), (56, 277), (0, 106)])
                    
# draw a line using draw.line()
# method of pygame.
# pygame.draw.line(surface, color,
# start point, end point, thickness) 
# pygame.draw.line(display_surface, green,
#                 (60, 300), (120, 300), 4)

# draw a circle using draw.circle()
# method of pygame.
# pygame.draw.circle(surface, color,
# center point, radius, thickness) 
# pygame.draw.circle(display_surface,
#            green, (300, 50), 20, 0)

# draw a ellipse using draw.ellipse()
# method of pygame.
# pygame.draw.ellipse(surface, color,
# bounding rectangle, thickness) 
# pygame.draw.ellipse(display_surface, black,
#                     (300, 250, 40, 80), 1)

# draw a rectangle using draw.rect()
# method of pygame.
# pygame.draw.rect(surface, color,
# rectangle tuple, thickness)
# thickness of line parameter is optional.

# board
pygame.draw.rect(display_surface, black,
                    (50, 50, 400, 400))
for x in range(10):
    pos = 50 + x * 40
    pygame.draw.line(display_surface, white,
                    (pos, 50), (pos, 450), 2)
    pygame.draw.line(display_surface, white,
                    (50, pos), (450, pos), 2)

apples = []
apples.append((1,1,'green'))
apples.append((3,5,'green'))
apples.append((7,8,'red'))

for apple in apples:
    x = 50 + apple[0] * 40 + 2
    y = 50 + apple[1] * 40 + 2
    pygame.draw.rect(display_surface, apple[2],
                        (x, y, 38, 38))

snake = []
snake.append((0,0))
snake.append((0,1))
snake.append((0,2))
snake.append((1,2))
snake.pop(0)

for s in range(len(snake)):
    x = 50 + snake[s][0] * 40 + 2
    y = 50 + snake[s][1] * 40 + 2
    pygame.draw.rect(display_surface, blue,
                        (x, y, 38, 38))
    if s == len(snake) - 1:
        pygame.draw.circle(display_surface,
                white, (x + 20, y + 20), 2, 0)

# infinite loop
while True :
    
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get() :

        

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT :

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen. 
        pygame.display.update()