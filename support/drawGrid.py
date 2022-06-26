import pygame


def draw_grid(window, block_width, block_height, mouse_position, x_grid_position_array, y_grid_position_array, increment):
    """Function to draw the background grid of the game.

    :param window: The window object used to display the game.
    """
    # Initialize variables
    temp_x_array_1 = []
    temp_x_array_2 = []
    temp_y_array_1 = []
    temp_y_array_2 = []
    delta_x = block_width / 2
    delta_y = block_height / 2
    minimum_y_index = None
    minimum_x_index = None

    # Define line color in RGB
    line_color = (180, 180, 180)
    # Grab the window dimensions.
    display_width, display_height = pygame.display.get_surface().get_size()

    # Increase cell width and height by 2 pixels.
    cw = block_width + increment
    ch = block_width + increment

    counter = 0
    for x in x_grid_position_array:
        if abs(x - mouse_position[0]) < delta_x:
            delta_x = abs(x - mouse_position[0])
            minimum_x_index = counter

        counter += 1

    counter = 0
    for y in y_grid_position_array:

        if abs(y - mouse_position[1]) < delta_y:
            delta_y = abs(y - mouse_position[0])
            minimum_y_index = counter

        counter += 1

    if x_grid_position_array[minimum_x_index] > mouse_position[0]:
        x_start = x_grid_position_array[minimum_x_index] + int(increment/2)
    else:
        x_start = x_grid_position_array[minimum_x_index] - int(increment/2)

    if y_grid_position_array[minimum_y_index] > mouse_position[1]:
        y_start = y_grid_position_array[minimum_y_index] - int(increment/2)
    else:
        y_start = y_grid_position_array[minimum_y_index] + int(increment/2)

    # Draw vertical lines beginning at the origin and ending at the height of the window
    for x_position in range(x_start, display_width, cw):
        pygame.draw.line(window, line_color, (x_position, 00), (x_position, display_height), 1)
        temp_x_array_1.append(x_position)

    for x_position in range(x_start, 0, -cw):
        pygame.draw.line(window, line_color, (x_position, 00), (x_position, display_height), 1)
        temp_x_array_2.append(x_position)

    # Draw horizontal lines beginning at the origin and ending at the width of the window
    for y_position in range(y_start, display_height, ch):
        pygame.draw.line(window, line_color, (00, y_position), (display_width, y_position), 1)
        temp_y_array_1.append(y_position)

    for y_position in range(y_start, 0, -ch):
        pygame.draw.line(window, line_color, (00, y_position), (display_width, y_position), 1)
        temp_y_array_2.append(y_position)

    temp_x_array_2.reverse()
    temp_y_array_2.reverse()

    temp_x_array_2.extend(temp_x_array_1)
    temp_y_array_2.extend(temp_y_array_1)

    x_grid_position_array = [temp_x_array_2[index] for index, i in enumerate(temp_x_array_2) if index < len(temp_x_array_2) -1]
    y_grid_position_array = [temp_y_array_2[index] for index, i in enumerate(temp_y_array_2) if index < len(temp_y_array_2) -1]

    return cw, ch, x_grid_position_array, y_grid_position_array
