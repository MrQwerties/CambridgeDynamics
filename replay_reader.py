import numpy as np
from PIL import ImageGrab
from keyboard_send import *
import time
from tetris_board import *
from tetris_lookahead import possible_locations
import os.path

default_x0 = 756
default_y0 = 856
default_square_size = 30
default_height = 20
default_width = 10

colors = {'#0f9bd7': 'I', '#2141c6': 'J', '#e35b02': 'L', '#e39f02': 'O',
          '#59b101': 'S', '#af298a': 'T', '#d70f37': 'Z'}
alt_colors = {'#170900': 'L', '#6b071b': 'S', '#9d257c': 'T', '#c10d31': 'Z'}
preview_colors = {'#074d6b': 'I', '#102063': 'J', '#712d01': 'L', '#714f01': 'O',
                  '#2c5800': 'S', '#571445': 'T', '#6b071b': 'Z'}


def color_hex(r, g, b):
    return '#' + hex(65536 * r + 256 * g + b)[2:].zfill(6)


def print_board(board):
    print('\n'.join(''.join(' X'[col[::-1][i]] for col in board) for i in range(len(board[0]))))


def read_hold(screenshot):
    r, g, b = screenshot[default_square_size + default_square_size//2][default_square_size//2]
    if (r, g, b) == (0, 0, 0):
        r, g, b = screenshot[default_square_size * 2 + default_square_size//2][default_square_size//2]
    if (r, g, b) == (0, 0, 0):
        return ' '
    h = color_hex(r, g, b)
    if h in colors.keys():
        return colors[h]
    return alt_colors[h]


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


def read_active(screenshot):
    for x in range(10):
        r, g, b = screenshot[(default_height - 19) * default_square_size - default_square_size // 2] \
            [(x + 3) * default_square_size + default_square_size // 2]
        if (r, g, b) != (0, 0, 0):
            return colors[color_hex(r, g, b)]
    return ' '


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

    if move is None:
        print_board(board)
        print(hold)
        print(queue)
        print(active_piece)
        print_board(next_board)
    return board, hold, queue, active_piece, 'MOVE', move[:3]


def piece_list(shape):
    shapes = 'IJLOSTZ '
    result = [0 for i in range(8)]
    result[shapes.index(shape)] = 1
    return result[:7]


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


def read_replay(game_id):
    time.sleep(2)
    click(561, 52)
    key_down(VK_CONTROL)
    key_down(KEY_A)
    key_up(VK_CONTROL)
    key_up(KEY_A)
    key_write('https://jstris.jezevec10.com/replay/' + str(game_id) + '?forceSkin=0')
    key_press(VK_RETURN)
    time.sleep(15)
    click(1310, 182)
    time.sleep(0.1)
    for _ in range(5):
        click(1528, 818)
        time.sleep(0.2)
    click(810, 700)
    time.sleep(0.1)
    click(695, 726)
    for _ in range(5):
        key_press(VK_LEFT)
        time.sleep(0.01)
    for _ in range(5):
        click(1528, 81)
        time.sleep(0.2)

    time.sleep(3)
    game = []
    last_time_sc = None
    time_sc = None
    first_piece = None
    repeated = 0
    while repeated < 3:
        last_time_sc = time_sc
        sc = np.array(ImageGrab.grab(bbox=(default_x0 - 3 * default_square_size, default_y0 - 20 * default_square_size,
                                           default_x0 + 13 * default_square_size, default_y0)))
        if isinstance(time_sc, type(None)):
            first_piece = read_active(sc)
            print('First piece: ' + first_piece)
        key_press(VK_RIGHT)
        game.append(read_game(sc))
        time.sleep(0.02)
        time_sc = np.array(ImageGrab.grab(bbox=(923, 908, 1024, 929)))

        if isinstance(last_time_sc, np.ndarray):
            if np.array_equal(last_time_sc, time_sc):
                repeated += 1
            else:
                repeated = 0
    # print(sum(last_time_sc))
    # print(sum(time_sc))
    # f = open('replays/game0.txt', 'w')
    # f.write(repr(game))
    # f.close()

    if not first_piece:
        return

    for i in range(len(game)):
        game[i] = (clean_board(game[i][0]), game[i][1], game[i][2])

    states = [tuple(game[0]) + (first_piece,)]
    last_queue = game[0][2]
    last_hold = game[0][1]
    active_piece = last_queue[0]
    for (board, hold, queue) in game[1:]:
        if queue != last_queue or hold != last_hold:
            if len(states):
                states[-1] += (active_piece,)
            states.append((board, hold, queue))
            if hold != last_hold:
                if last_hold == ' ':
                    active_piece = last_queue[0]
                else:
                    active_piece = last_hold
            elif queue != last_queue:
                active_piece = last_queue[0]
        last_queue = queue
        last_hold = hold

    data = []
    for i in range(len(states) - 1):
        try:
            data.append(make_example(states[i][0], states[i][1], states[i][2], states[i][3],
                                     states[i + 1][0], states[i + 1][1]))
        except TypeError:
            pass
        print(i)

    f = open('training_data_ultra_complete/game' + str(game_id) + '.txt', 'w')
    f.write('\n'.join(format_data(example) for example in data))
    f.close()


if __name__ == '__main__':
    code = open('ultra_leaderboard.html', 'r', encoding='utf-8').read()
    for i in code.split('<a href="https://jstris.jezevec10.com/replay/')[1:]:
        game_id = int(i[:i.index('"')])
        if not os.path.exists('training_data_ultra_complete/game' + str(game_id) + '.txt'):
            read_replay(game_id)
