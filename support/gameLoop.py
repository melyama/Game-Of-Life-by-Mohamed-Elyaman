import pygame
import sys
import time


def main_game(window, cell_width, cell_height):

    # Initialize a 2D array with False to represent initial state of all cells
    array = array_init(cell_width, cell_height)
    run = False
    space_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            user_select_cells(event, window, array, cell_width, cell_height)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_count += 1
                    if space_count % 2 != 0:
                        run = True
                    else:
                        run = False

        if run:
            run_game(window, array, cell_width, cell_height)

        pygame.display.update()


def to_alive(window, array, mouse_position, cell_width, cell_height):
    """Switch a cell state from dead to alive.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).
    :param: mouse_position: The position of the user's mouse when a click has occurred (if it has occurred).

    :return: Void. No return, set the corresponding array value to True and color the respective cell yellow.
    """
    # Define the cell color when alive.
    alive_cell_color = (255, 255, 0)

    # Get the x and y positions of the top left hand corner of the cell or cell.
    x_position = mouse_position[0] - (mouse_position[0] % cell_width)
    y_position = mouse_position[1] - (mouse_position[1] % cell_height)

    pygame.draw.rect(window, alive_cell_color, (x_position + 1, y_position + 1, cell_width - 1, cell_height -1))

    col = int(x_position / cell_width)
    row = int(y_position / cell_height)

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

    col = int(x_position / cell_width)
    row = int(y_position / cell_height)

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
    # by the width and height of a single cell.
    cols = int(w/cell_width)
    rows = int(h/cell_height)
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
    inverse_indices = []
    for i in range(0, len(array) - 1):
        for j in range(0, len(array[0]) - 1):
            if cell_die_or_live(get_live_neighbors(array, i, j), i, j, array[i][j]):
                inverse_indices.append(cell_die_or_live(get_live_neighbors(array, i, j), i, j, array[i][j]))

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
    count = 0
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


    :return: Void. Draw the reversed state of the cell and update the Array reference to reverse cell state at the given position.
        """
    if cell[2]:
        color = (128, 128, 128)
        array[cell[0]][cell[1]] = not cell[2]
    else:
        color = (255, 255, 0)
        array[cell[0]][cell[1]] = not cell[2]

    pygame.draw.rect(window, color, (cell[1] * cell_width + 1, cell[0] * cell_height + 1, cell_width - 1,
                                                cell_height - 1))


def run_game(window, array, cell_width, cell_height):
    """Run the game logic in a while loop.

    :param: window: The pygame window object that display's the game.
    :param: array: The boolean array that stores the state of each cell.
    :param: cell_width: The width of a single cell (cell).
    :param: cell_height: The height of a single cell (cell).

    :return: Void. Run the game logic."""
    game_logic(window, array, cell_width, cell_height)
    time.sleep(0.1)


def user_select_cells(event, window, array, cell_width, cell_height):

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            to_alive(window, array, pygame.mouse.get_pos(), cell_width, cell_height)
        elif event.button == 3:
            to_dead(window, array, pygame.mouse.get_pos(), cell_width, cell_height)