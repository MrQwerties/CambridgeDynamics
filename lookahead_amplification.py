from tetris_lookahead import possible_locations
from tetris_board import *


def score(board, hold, queue, active, can_hold, board_func, place_func, depth):
    if depth == 0:
        return board_func(board)

    moves = []
    for x, y, s, m in possible_locations(TetrisPiece(active, 4, 19, 0), board):
        test_board = TetrisBoard(board.width, board.height)
        test_board.board = [line[:] for line in board.board]
        new_piece = TetrisPiece(active, x, y, s)
        h = place_func(test_board, new_piece)
        test_board.piece_add(new_piece)
        test_board.check_clear()

        moves.append((test_board, h, 'move'))

    if can_hold:
        moves.append((board, 0, 'hold'))

    record = None
    for test_board, h, action in moves:
        if action == 'move':
            s = h + score(test_board, hold, queue[1:], queue[0], True, board_func, place_func, depth - 1)
        elif action == 'hold':
            s = score(board, active, queue, hold, False, board_func, place_func, depth - 1)
        if record is None or s > record:
            record = score

    return record
