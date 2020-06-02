import itertools
from tetris_board import *


def possible_locations(piece, board):
    states = itertools.product(range(-1, board.width), range(board.height + 1), range(4))
    reached = {}
    for (i, j, s) in states:
        reached[(i, j, s)] = False
    reached[(piece.x, piece.y, piece.state)] = True
    to_check = [(piece.x, piece.y, piece.state, '')]
    possible = []

    while to_check:
        x, y, s, m = to_check.pop(0)
        if TetrisPiece(piece.shape, x, y, s).on_ground(board):
            possible.append((x, y, s, m))

        new_states = []

        # Translations
        new_piece = TetrisPiece(piece.shape, x, y, s)
        #positions = ((-1, 0, 'L'), (1, 0, 'R'), (0, -1, 'd'))
        positions = ((-1, 0, 'l'), (1, 0, 'r'))
        for dx, dy, dm in positions:
            if board.piece_fits(new_piece, dx, dy):
                new_states.append((x + dx, y + dy, s, m + dm))

        # Drops
        drops = ((0, -1, 'D'), (1, 0, 'R'), (-1, 0, 'L'))
        for d in drops:
            dropped_piece = TetrisPiece(piece.shape, x, y, s)
            dropped_piece.soft_drop(board, d[0], d[1])
            new_states.append((dropped_piece.x, dropped_piece.y, dropped_piece.state, m + d[2]))

        # Rotations
        cw_piece = TetrisPiece(piece.shape, x, y, s)
        if cw_piece.rotate((s + 1) % 4, board):
            new_states.append((cw_piece.x, cw_piece.y, cw_piece.state, m + 'x'))
        ccw_piece = TetrisPiece(piece.shape, x, y, s)
        if ccw_piece.rotate((s - 1) % 4, board):
            new_states.append((ccw_piece.x, ccw_piece.y, ccw_piece.state, m + 'z'))

        # Add newly reached states to queue
        for x_new, y_new, s_new, m_new in new_states:
            if not reached[(x_new, y_new, s_new)]:
                reached[(x_new, y_new, s_new)] = True
                to_check.append((x_new, y_new, s_new, m_new))
    return possible


def best_place(queue, board, board_func=lambda b: b.stack_height(), place_func=lambda b, p: 0, branch_factor=2):
    record = -1
    best_sequence = ''
    moves = []
    for x, y, s, m in possible_locations(TetrisPiece(queue[0], 4, 19, 0), board):
        test_board = TetrisBoard(board.width, board.height)
        test_board.board = [line[:] for line in board.board]
        new_piece = TetrisPiece(queue[0], x, y, s)
        h = place_func(test_board, new_piece)
        test_board.piece_add(new_piece)
        h -= 2 * test_board.check_clear()

        moves.append(((test_board, m), h + board_func(test_board), h))

    moves.sort(key=lambda p: p[1])
    for m in moves[:min(branch_factor, len(moves))]:
        test_board, seq = m[0]
        h = m[2]
        if len(queue) > 1:
            h += best_place(queue[1:], test_board, board_func, place_func, branch_factor)[1]
        else:
            h += board_func(test_board)

        if h < record or record == -1:
            record = h
            best_sequence = seq
    return best_sequence, record
