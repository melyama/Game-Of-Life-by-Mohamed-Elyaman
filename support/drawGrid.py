import pygame


def draw_grid(window, block_width, block_height, mouse_position=(0,0)):
    """Function to draw the background grid of the game.

    :param window: The window object used to display the game.
    """
    # Define line color in RGB
    line_color = (180, 180, 180)
    # Grab the window dimensions.
    display_width, display_height = pygame.display.get_surface().get_size()

    # Initialise Box position dictionary

    # Draw vertical lines beginning at the origin and ending at the height of the window
    for x_position in range(mouse_position[0], display_width, block_width):
        pygame.draw.line(window, line_color, (x_position, 00), (x_position, display_height), 1)

    for x_position in range(mouse_position[0], 0, -block_width):
        pygame.draw.line(window, line_color, (x_position, 00), (x_position, display_height), 1)

    # Draw horizontal lines beginning at the origin and ending at the width of the window
    for y_position in range(mouse_position[1], display_width, block_height):
        pygame.draw.line(window, line_color, (00, y_position), (display_width, y_position), 1)

    for y_position in range(mouse_position[1], 0, -block_height):
        pygame.draw.line(window, line_color, (00, y_position), (display_width, y_position), 1)
