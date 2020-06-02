import numpy as np
from PIL import ImageGrab
from keyboard_send import *
import time

default_x0 = 756
default_y0 = 856
default_square_size = 30
default_height = 20
default_width = 10

colors = {'#0f9bd7': 'I', '#2141c6': 'J', '#e35b02': 'L', '#e39f02': 'O',
          '#59b101': 'S', '#af298a': 'T', '#d70f37': 'Z'}
preview_colors = {'#074d6b': 'I', '#102063': 'J', '#712d01': 'L', '#714f01': 'O',
                  '#2c5800': 'S', '#571445': 'T', '#6b071b': 'Z'}


def color_hex(r, g, b):
    return '#' + hex(65536 * r + 256 * g + b)[2:].zfill(6)


def print_board(board):
    print('\n'.join(''.join(' X'[col[::-1][i]] for col in board) for i in range(len(board[0]))))


def read_hold(screenshot):
    r, g, b = screenshot[default_square_size + default_square_size//2][default_square_size//2]
    if r == 0 and g == 0 and b == 0:
        r, g, b = screenshot[default_square_size * 2 + default_square_size//2][default_square_size//2]
    return colors[color_hex(r, g, b)]


def read_board(screenshot):
    board = [[0]*default_height for _ in range(default_width)]
    for i in range(default_width):
        for j in range(default_height):
            r, g, b = screenshot[(default_height - j) * default_square_size - default_square_size//2]\
                [(i + 3) * default_square_size + default_square_size//2]
            if color_hex(r, g, b) in colors.keys():
                board[i][j] = 1
            elif color_hex(r, g, b) != '#000000':
                board[i][j] = -1
    return board


def read_queue(screenshot):
    queue = []

    for i in range(5):
        r, g, b = screenshot[default_square_size * (3 * i + 1) + default_square_size//2]\
            [default_square_size * 15 + default_square_size//2]
        if r == 0 and g == 0 and b == 0:
            r, g, b = screenshot[default_square_size * (3 * i + 2) + default_square_size//2]\
                [default_square_size * 15 + default_square_size//2]
        queue.append(colors[color_hex(r, g, b)])
    return queue


def read_game(screenshot):
    return (read_board(screenshot), read_hold(screenshot), read_queue(screenshot))


time.sleep(3)
game = []
for i in range(100):
    sc = np.array(ImageGrab.grab(bbox=(default_x0 - 3 * default_square_size, default_y0 - 20 * default_square_size,
                                           default_x0 + 13 * default_square_size, default_y0)))
    game.append(read_game(sc))
    key_press(VK_RIGHT)
f = open('replays/game0.txt', 'w')
f.write(repr(game))
f.close()
