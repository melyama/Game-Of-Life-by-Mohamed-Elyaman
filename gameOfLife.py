import pygame
from support.drawGrid import draw_grid
from support.gameLoop import main_game


def main():
    """Main game function, run this file to play the game. This code was written by Mohamed Elyaman.

    This is a personal copy of the game of life created by  the English Mathematician John Conway.
    The game operates by the following simple rules:

    1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    2. Any live cell with two or three live neighbors lives on to the next generation.
    3. Any live cell with more than three live neighbors dies as if by overpopulation.
    4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

    To play the game run this file, then select the cells to revive with left click. If you wish to undo a cell,
    use the right click button on the mouse. Once the selection process is completed, press space bar once to run
    the game logic.

    If you desire to pause/stop the game logic, simply press space bar a second time. If you would like to restart, either
    deselect the cells you want to remove using right click or exit the game by clicking the exit button on the top
    right hand corner of the window and re-run this program.

    """
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


if __name__ == '__main__':
    main()
