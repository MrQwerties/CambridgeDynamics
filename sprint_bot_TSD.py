from tetris_lookahead import *
from tetris_board import *
from tetris_screen_grabber import *
from keyboard_send import *
import numpy as np
from PIL import ImageGrab
from tetris_display import *
#import pyautogui
import time


def print_board(board):
    print('\n'.join(''.join(' X'[col[::-1][i]] for col in board) for i in range(len(board[0]))))


def column_height(column):
    if True in column:
        return len(column) - 1 - column[::-1].index(True)
    return 0


def column_func(board):
    heights = [column_height(col) for col in board.board]
    return sum((heights[i + 1] - heights[i])**2 for i in range(len(heights) - 1))


def num_holes(board):
    total = 0
    for column in board.board:
        top_found = False
        for r in column[::-1]:
            if r:
                top_found = True
            else:
                total += top_found
    return total


def combine_func(board):
    return 0.5 * board.stack_height() + 2 * num_holes(board)


def lowest_board(piece, board, func=lambda b: b.stack_height()):
    record = -1
    best_sequence = ''
    best_board = None
    for x, y, s, m in possible_locations(piece, board):
        test_board = TetrisBoard(board.width, board.height)
        test_board.board = [line[:] for line in board.board]
        test_board.piece_add(TetrisPiece(piece.shape, x, y, s))
        test_board.check_clear()
        h = func(test_board)
        if h < record or record == -1:
            record = h
            best_sequence = m
            best_board = test_board
    return best_sequence, record, best_board


def press_sequence(sequence):
    keys = {'l': VK_LEFT, 'r': VK_RIGHT, 'D': VK_DOWN, 'x': KEY_X, 'z': KEY_Z}
    for i, char in enumerate(sequence):
        if char == 'D':
            if i == len(sequence) - 1:
                break
            else:
                key_press(VK_DOWN, 0.02)
        elif char == 'R':
            key_press(VK_RIGHT, 0.04)
        elif char == 'L':
             key_press(VK_LEFT, 0.04)
        else:
            key_press(keys[char])
            time.sleep(0.03)
    key_press(VK_SPACE)
    time.sleep(0.03)


def read_queue():
    queue = []
    screenshot = np.array(ImageGrab.grab(bbox=(864, 248, 866, 660)))

    for i in range(5):
        r, g, b = screenshot[default_square_size * 3 * i + 15][1]
        if r == 0 and g == 0 and b == 0:
            r, g, b = screenshot[default_square_size * (3 * i + 1) + 15][1]
        queue.append(colors['#' + hex(65536 * r + 256 * g + b)[2:].zfill(6)])
    return queue


time.sleep(3)
key_press(KEY_P)
time.sleep(1)
queue = read_queue()
time.sleep(0.9)
board = TetrisBoard(10, 22)
c = 0
while True:
    # if seen_board.board != board.board:
    #     print('ERROR')
    #     print('EXPECTED:')
    #     print_board(board.board)
    #     print('\nGOT:')
    #     print_board(seen_board.board)
    #     print()
    #     print(shape)
    #     print(seq)

    screenshot = np.array(ImageGrab.grab(bbox=(490, 218, 790, 812)))
    board = make_board(screenshot, default_x0, default_y0, default_square_size, default_width, 22, 19)
    seq, score = best_place(queue[:2], board, combine_func)
    queue = read_queue()
    press_sequence(seq)
