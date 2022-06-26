import pygame


def default_draw_grid(window, block_width, block_height):
    """Function to draw the background grid of the game.
    :param window: The window object used to display the game.
    """
    x = []
    y = []

    # Define line color in RGB
    line_color = (180, 180, 180)

    # Grab the window dimensions.
    w, h = pygame.display.get_surface().get_size()

    # Initialise Box position dictionary

    # Draw vertical lines beginning at the origin and ending at the height of the window
    for i in range(0, w, block_width):
        pygame.draw.line(window, line_color, (i, 00), (i, h), 1)
        x.append(i)

    # Draw horizontal lines beginning at the origin and ending at the width of the window
    for i in range(0, w, block_height):
        pygame.draw.line(window, line_color, (00, i), (w, i), 1)
        y.append(i)

    return x, y
