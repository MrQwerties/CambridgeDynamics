import numpy as np
from PIL import ImageGrab
from keyboard_send import *
import time
from tetris_board import *
from tetris_lookahead import possible_locations

default_x0 = 756
default_y0 = 856
default_square_size = 30
default_height = 20
default_width = 10

colors = {'#0f9bd7': 'I', '#2141c6': 'J', '#e35b02': 'L', '#e39f02': 'O',
          '#59b101': 'S', '#af298a': 'T', '#d70f37': 'Z', '#000000': ' '}
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
    return read_board(screenshot), read_hold(screenshot), read_queue(screenshot)


def clean_board(board):
    result = []
    for col in board:
        ghost = False
        new_col = []
        for i in col:
            if i == -1:
                ghost = True
            if ghost:
                new_col.append(0)
            else:
                new_col.append(i)
        result.append(new_col)
    return result


def make_example(board, hold, queue, active_piece, next_board, next_hold):
    if next_hold != hold:
        return board, hold, queue, active_piece, 'HOLD', (-1, -1, -1)
    piece = TetrisPiece(active_piece, 4, 19, 0)
    b = TetrisBoard(10, 24)
    b.set_board(board)

    move = None
    for (x, y, s, m) in possible_locations(piece, b):
        test_board = TetrisBoard(10, 24)
        test_board.board = [row[:] for row in b.board]
        test_board.piece_add(TetrisPiece(active_piece, x, y, s))
        test_board.check_clear()
        if [row[:20] for row in test_board.board] == next_board:
            if not move or len(m) < len(move[3]):
                move = (x, y, s, m)
            break

    if move == None:
        print_board(board)
        print(hold)
        print(queue)
        print(active_piece)
        print_board(next_board)
    return board, hold, queue, active_piece, 'MOVE', move[:3]


def piece_list(shape):
    shapes = 'IJLOSTZ'
    result = [0 for i in range(7)]
    result[shapes.index(shape)] = 1
    return result


def format_data(example):
    result = ', '.join(', '.join('1' if x else '0' for x in row) for row in example[0]) + ', '
    result += ', '.join(', '.join(str(x) for x in piece_list(piece)) for piece in
                        [example[1]] + example[2] + [example[3]]) + '|'

    answer = [0 for i in range(35)]
    if example[4] == 'HOLD':
        answer[0] = 1
    else:
        answer[1 + example[5][0]] = 1
        answer[11 + example[5][1]] = 1
        answer[31 + example[5][2]] = 1

    result += ', '.join(str(i) for i in answer)
    return result


time.sleep(3)
game = []
for i in range(1800):
    sc = np.array(ImageGrab.grab(bbox=(default_x0 - 3 * default_square_size, default_y0 - 20 * default_square_size,
                                           default_x0 + 13 * default_square_size, default_y0)))
    game.append(read_game(sc))
    key_press(VK_RIGHT)
    time.sleep(0.01)
# f = open('replays/game0.txt', 'w')
# f.write(repr(game))
# f.close()

for i in range(len(game)):
    game[i] = (clean_board(game[i][0]), game[i][1], game[i][2])

states = []
lastQueue = game[0][2]
lastHold = game[0][1]
activePiece = lastQueue[0]
for (board, hold, queue) in game[1:]:
    if queue != lastQueue or hold != lastHold:
        if len(states):
            states[-1] += (activePiece,)
        states.append((board, hold, queue))
        if hold != lastHold:
            activePiece = lastHold
        elif queue != lastQueue:
            activePiece = lastQueue[0]
    lastQueue = queue
    lastHold = hold

data = []
for i in range(len(states) - 1):
    try:
        data.append(make_example(states[i][0], states[i][1], states[i][2], states[i][3],
                             states[i + 1][0], states[i + 1][1]))
    except TypeError:
        pass
    print(i)

f = open('training_data_ultra/game9_example.txt', 'w')
f.write('\n'.join(format_data(example) for example in data))
f.close()
