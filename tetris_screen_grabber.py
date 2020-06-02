import numpy as np
from PIL import ImageGrab
from tetris_board import TetrisBoard

colors = {'#0f9bd7': 'I', '#2141c6': 'J', '#e35b02': 'L', '#e39f02': 'O',
          '#59b101': 'S', '#af298a': 'T', '#d70f37': 'Z'}

default_x0 = 15
default_y0 = 585
default_square_size = 30
default_width = 10
default_height = 20


def make_board(screenshot, x0, y0, square_size, width, height, max_read_height):
    """ make_board(2D Array of RGB values, int x0, int y0, int square_size, int width, int height)
    Makes a board corresponding to the one on screen.
    (x0, y0) is the location of a square on the lower left corner of the board on the screen.
    square_size is the size of the squares displayed
    width and height are the width and height of the board shown on screen. """
    board = TetrisBoard(width, height)
    #screenshot = np.array(ImageGrab.grab(bbox=(490, 218, 910, 812)))

    if max_read_height == -1:
        h = height
    else:
        h = min(height, max_read_height)
    for i in range(width):
        for j in range(h):
            board.board[i][j] = square_color(i, j, screenshot, x0, y0, square_size) in colors.keys()
    return board


def square_color(x, y, screenshot, x0, y0, square_size):
    """ square_color(int x, int y, 2D array screenshot, int x0, int y0, int square_size) -> RGB color string
    Returns the rgb color string of the square in the position (x, y), based on the screenshot. """
    r, g, b = screenshot[y0 - square_size * y][x0 + square_size * x]
    return '#' + hex(65536 * r + 256 * g + b)[2:].zfill(6)
