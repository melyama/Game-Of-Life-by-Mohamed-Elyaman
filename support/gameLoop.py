"""Main game loop module. Holds all of the game loop functions."""

import pygame
import sys
import time
from .drawGrid import draw_grid


def main_game(window, cell_width, cell_height):
    """Run the game loop.

   :param: window: The pygame window object that display's the game.
   :param: cell_width: The width of a single cell (cell).
   :param: cell_height: The height of a single cell (cell).

   :return: Void.
   """
    # Initialize a 2D array with False to represent initial state of all cells
    array = array_init(cell_width, cell_height)

    # Initialize a run variable to run game logic when user presses space.
    run = False

    # Initialize a space count variable to count the number of times a user presses space. Even numbers pause the
    # game, odd numbers resume.
    space_count = 0

    # Main game while loop.
    while True:
        # Check all the events and execute logic.
        run, space_count, cell_width, cell_height = check_events(window, array,
                                                                 cell_width, cell_height, run, space_count)

        # Check run variable. If true, run game logic.
        if run:
            run_game(window, array, cell_width, cell_height)

        # Update game display with new drawing.
        pygame.display.update()


def check_events(window, array, cell_width, cell_height, run, space_count):
    """Switch a cell state from dead to alive.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).
    :param: run: flag variable which stores whether game is in pause or run mode.
    :param: space_count: counter variable which holds how many times the space bar key has been pressed.

    :return: Void. No return, set the corresponding array value to True and color the respective cell yellow.
    """
    # Loop through all events (user inputs)
    for event in pygame.event.get():
        # If the user presses the quit button, exit the process.
        if event.type == pygame.QUIT:
            sys.exit()

        # Allow user to select cells to be dead or alive if and only if the game is paused.
        if not run:
            user_select_cells(window, array, cell_width, cell_height)
            user_increment_generation(event, window, array, cell_width, cell_height)

        # Allow the user to scroll to adjust size od the grid.
        cell_width, cell_height = user_scroll(window, array, event, cell_width, cell_height)

        # Check space count here and resume/pause game accordingly.
        run, space_count = check_space(event, space_count, run)

    return run, space_count, cell_width, cell_height


def to_alive(window, array, cell_width, cell_height,  mouse_position=None, cell_x_position=None, cell_y_position=None):
    """Switch a cell state from dead to alive.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).
    :param: mouse_position: The position of the user's mouse where a click has occurred.

    :return: Void. No return, set the corresponding array value to True and color the respective cell yellow.
    """
    # Define the cell color when alive.
    alive_cell_color = (255, 255, 0)

    # If the function is called with no mouse position input, draw the state of the array.
    if not mouse_position:
        pygame.draw.rect(window, alive_cell_color,
                         ((cell_x_position * cell_width) + 1,
                          (cell_y_position * cell_height) + 1, cell_width - 1, cell_height - 1))
        return

    # Get the x and y positions of the top left hand corner of the cell or cell.
    x_position = mouse_position[0] - (mouse_position[0] % cell_width)
    y_position = mouse_position[1] - (mouse_position[1] % cell_height)

    # Fill the cell with the color representing an alive state.
    pygame.draw.rect(window, alive_cell_color, (x_position + 1, y_position + 1, cell_width - 1, cell_height -1))

    # Get the row and column of the cell by dividing the x-position and y-position of the cell
    # by the width and height of a single cell. Cast to an integer for indexing.
    col = int(x_position / cell_width)
    row = int(y_position / cell_height)

    # Set the cell value in the array to True for alive.
    array[row][col] = True


def to_dead(window, array, mouse_position, cell_width, cell_height):
    """Switch a cell state from alive to dead.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).
    :param: mouse_position: The position of the Users mouse when a click has occurred (if it has occurred).

    :return: Void. No return, set the corresponding array value to False and color the respective cell yellow.
    """
    # Define the cell color when alive.
    dead_cell_color = (128, 128, 128)

    x_position = mouse_position[0] - (mouse_position[0] % cell_width)
    y_position = mouse_position[1] - (mouse_position[1] % cell_height)

    pygame.draw.rect(window, dead_cell_color, (x_position + 1, y_position + 1, cell_width - 1, cell_height - 1))

    # Get the row and column of the cell by dividing the x-position and y-position of the cell
    # by the width and height of a single cell. Cast to an integer for indexing.
    col = int(x_position / cell_width)
    row = int(y_position / cell_height)

    # Set the cell value in the array to False for dead.
    array[row][col] = False


def array_init(cell_width, cell_height):
    """Initialize a 2D array of 'False' values to represent the state of all cells at the beginning of the game.

    :param: cell_width: The width of a single cell.
    :param: cell_height: The height of a single cell.

    :return: array: The initialized array.
    """
    # Get display width and height. 
    w, h = pygame.display.get_surface().get_size()
    
    # Get the total rows and columns of the array by dividing the width and height of the game display
    # by the width and height of a single cell. Cast to an integer for indexing.
    cols = int(w/cell_width)
    rows = int(h/cell_height)

    # Create an array of size rows x cols and fill it with the value 'False'
    array = [[False for i in range(cols)] for j in range(rows)]

    return array


def game_logic(window, array, cell_width, cell_height):
    """Check each cell and determine whether it's value should be inverted. invert cell values accordingly.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void. Reverse cell values in the array object where needed.
    """
    # Initialize empty array to hold the coordinates of cells whose value needs to be inverted.
    inverse_indices = []

    # Loop through the entire array, going row by row. Check whether each cell's state should remain the same
    # or be inverted. If a cell's state should be inverted, store the index of that cell in the initialized array.
    for i in range(0, len(array) - 1):
        for j in range(0, len(array[0]) - 1):
            if cell_die_or_live(get_live_neighbors(array, i, j), i, j, array[i][j]):
                inverse_indices.append(cell_die_or_live(get_live_neighbors(array, i, j), i, j, array[i][j]))

    # Loop through the array of cell indices and invert the value of each cell.
    for cell in inverse_indices:
        inverse_cell_state(cell, window, array, cell_width, cell_height)


def get_live_neighbors(array, row, col):
    """Get the number of 'alive' neighbors of a cell.

    A neighbor is any cell that is directly adjacent to the cell in question. Diagonals included.
    All cells have 9 neighbors.

    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: array: The initialized array.
    """
    # Initialize a count variable to count the number of alive neighbors found.
    count = 0

    # Loop through the surrounding cells (above, below, to the left and to the right) and check whether each cell is
    # alive or not. If a neighbor cell is alive, increment count.
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i != row) or (j != col):
                if array[i][j]:
                    count += 1
    return count


def cell_die_or_live(live_neighbors, row, column, state):
    """Determine whether a cell will die, be revived or remain the same.

    :param: live_neighbors: The number of alive neighbors the cell has.
    :param: row: row value of the cell.
    :param: row: column value of the cell.
    :param: state: current state of the cell. False for dead, True for alive.


    :return: cell index if cell will die or be revived.
    :return: False if cell is to reman the same.
    """
    # Check whether a cell should be inverted. If a cell's properties falls within any of the rules and needs to be
    # inverted, return the cell's index along with it's current state.
    if live_neighbors < 2 and state:
        return [row, column, state]
    elif live_neighbors > 3 and state:
        return [row, column, state]
    elif live_neighbors == 3 and not state:
        return [row, column, state]

    return False


def inverse_cell_state(cell, window, array, cell_width, cell_height):
    """Inverse the state of any given cell.

    :param: cell: The cell position to inverse.
    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).


    :return: Void. Draw the reversed state of the cell and update the Array
    reference to reverse cell state at the given position.
    """
    # Check the state of a cell. If it is True, invert it and fill in the corresponding cell on the display with
    # the dead color. If it is False, invert it and fill in the corresponding cell on the display
    # with the alive color.
    if cell[2]:
        color = (128, 128, 128)
        array[cell[0]][cell[1]] = not cell[2]
    else:
        color = (255, 255, 0)
        array[cell[0]][cell[1]] = not cell[2]

    # Fill in the cell on the display.
    pygame.draw.rect(window, color, (cell[1] * cell_width + 1, cell[0] * cell_height + 1, cell_width - 1,
                                                cell_height - 1))


def run_game(window, array, cell_width, cell_height):
    """Run the game logic in a while loop.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void. Run the game logic."""
    # Run game logic
    game_logic(window, array, cell_width, cell_height)

    # Sleep for 0.1 seconds to slow down the animation.
    time.sleep(0.01)


def user_select_cells(window, array, cell_width, cell_height):
    """Allow user to select and deselect cells.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void."""
    # Check if mouse is pressed. If the left click is pressed (0), set the state of the cell under the mouse's position
    # to alive. If the right click is pressed (2), set the state of the cell under the mouses position to dead.
    if pygame.mouse.get_pressed()[0]:
        to_alive(window, array, cell_width, cell_height, pygame.mouse.get_pos())
    elif pygame.mouse.get_pressed()[2]:
        to_dead(window, array, pygame.mouse.get_pos(), cell_width, cell_height)


def check_space(event, space_count, run):
    """Check user input for space bar.

    If space bar is pressed once, play the game. Twice, pause the game. Alternate to allow user to play/pause game as
    needed.

    :param: event: The event object that keeps track of user inputs.
    :param: space_count: A variable keeping track of the number of times space has been pressed.

    :return: Void."""
    # Check if a key has been pressed. If he pressed key is space bar, check whether the occurrence is odd or even.
    # If the occurrence is odd, return True and the value of space_count. If the occurrence is odd, return False and
    # the value of space_count.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            space_count += 1
            if space_count % 2 != 0:
                return True, space_count
            else:
                return False, space_count

    # If nothing has changed, return original run and space values.
    return run, space_count


def user_scroll(window, array, event, cell_width, cell_height):
    """Adjust the size of cells and redraw the new size if the user uses the mouse scroll.

    If the user scrolls in, increase the size of each cell on the display screen. If the user scrolls out, decrease the
    size of each cell on the display screen.

    :param: event: The event object that keeps track of user inputs.
    :param: space_count: A variable keeping track of the number of times space has been pressed.

    :return: Void."""
    # Check if the current event involved a mouse button.
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the event that occurred is a mouse scroll in. If so, increase cell size to zoom in.
        if event.button == 4:
            # Increase cell width and height by 2 pixels.
            cell_width += 2
            cell_height += 2

            # Refill the window with the background color before drawing new grid.
            # If so, increase cell size to zoom out.
            window.fill((128, 128, 128))
            # Draw new grid and update the display.
            draw_grid(window, cell_width, cell_height)
            draw_array_state(window, array, cell_width, cell_height)
            pygame.display.update()

            return cell_width, cell_height

        # Check if the event that occurred is a mouse scroll out.
        elif event.button == 5:
            # Reduce cell width and height by 2 pixels.
            cell_width -= 2
            cell_height -= 2

            # Refill the window with the background color before drawing new grid.
            window.fill((128, 128, 128))
            # Draw new grid and update the display.
            draw_grid(window, cell_width, cell_height)
            draw_array_state(window, array, cell_width, cell_height)
            pygame.display.update()

            return cell_width, cell_height

    # If nothing has changed, return original cell width and height.
    return cell_width, cell_height


def draw_array_state(window, array, cell_width, cell_height):
    """Draw the current state of the array onto the display.

    Loop through the current array. Where there is a True, draw a corresponding yellow block on the display to
    represent an alive cell.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void."""
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            if array[i][j]:
                to_alive(window, array, cell_width, cell_height, cell_x_position=j, cell_y_position=i)
    return


def user_increment_generation(event, window, array, cell_width, cell_height):
    """Allow user to increment by one generation if left key button is clicked during pause mode.

    Check if left key is down. If true, increment the game by one generation.

    :param: event: The event object that keeps track of user inputs.
    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            run_game(window, array, cell_width, cell_height)