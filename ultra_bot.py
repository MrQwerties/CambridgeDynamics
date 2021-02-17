from replay_reader import *
import time
from PIL import ImageGrab
import tensorflow as tf
import numpy as np
from keyboard_send import *
from tetris_lookahead import *


def action(number):
    if number == 800:
        return 'HOLD', (-1, -1, -1)
    return 'MOVE', (number//80, (number//4)%20, number%4)


def press_sequence(sequence):
    keys = {'l': VK_LEFT, 'r': VK_RIGHT, 'D': VK_DOWN, 'x': KEY_X, 'z': KEY_Z}
    for i, char in enumerate(sequence):
        if char == 'D':
            if i == len(sequence) - 1:
                break
            else:
                key_press(VK_DOWN, 0.1)
        elif char == 'R':
            key_press(VK_RIGHT, 0.1)
        elif char == 'L':
            key_press(VK_LEFT, 0.1)
        else:
            key_press(keys[char])
            time.sleep(0.05)
    key_press(VK_SPACE)
    time.sleep(0.05)


model = tf.keras.models.load_model('saved_models/cnn-0')

default_x0 = 490
default_y0 = 815
default_square_size = 30

time.sleep(3)
key_press(KEY_P)
time.sleep(2.1)

changed_hold = False
for i in range(80):
    sc = np.array(ImageGrab.grab(bbox=(default_x0 - 3 * default_square_size, default_y0 - 20 * default_square_size,
                                           default_x0 + 13 * default_square_size, default_y0)))
    board = clean_board(read_board(sc))
    active = read_active(sc)
    hold = read_hold(sc)
    queue = read_queue(sc)
    blocks = np.array([piece_list(x) for x in [hold] + queue + [active]]).flatten()

    prediction = model({'board': np.array([board]), 'blocks': np.array([blocks])}).numpy()
    if not changed_hold and np.argmax(prediction) == 800:
        time.sleep(0.5)
        key_press(KEY_C)
        changed_hold = True
        print(prediction[0][800])
        print(active)
        print('HOLD')
        print()
    else:
        b = TetrisBoard(10, 24)
        b.set_board(board)
        move = ''
        best = None
        action = None
        for (x, y, s, m) in possible_locations(TetrisPiece(active, 4, 19, 0), b):
            score = prediction[0][4 * (20 * x + y) + s]
            if best is None or score > best:
                best = score
                action = (x, y, s)
                move = m
        print(score)
        print(active)
        print(action)
        print()
        press_sequence(move)
        changed_hold = False
    time.sleep(0.1)
