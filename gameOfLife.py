# Importing pygame module
import pygame
from drawGrid import draw_grid
from gameLoop import main_game
from pygame.locals import *

# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# create the display surface object
# of specific dimension.
width = 1920
height = 1080
window = pygame.display.set_mode((1920, 1080))
# Create a block size to divide the display into a grid.
block_width = 30
block_height = 30

# Fill the scree with a grey background color
window.fill((128, 128, 128))


# Draws the surface object to the screen.
draw_grid(window, block_width, block_height)
main_game(window, block_width, block_height)
