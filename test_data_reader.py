from tetris_board import print_board

def parse_example(example):
    shapes = 'IJLOSTZ'

    data, answer = ([int(x) for x in part.split(', ')] for part in example.split('|'))
    board_data = data[:200]
    pieces_data = [data[200 + 7 * i:200 + 7 * (i + 1)] for i in range(7)]

    board = []
    for i in range(10):
        board.append([])
        for j in range(20):
            board[i].append(board_data[20 * i + j])

    hold = shapes[pieces_data[0].index(1)]
    queue = [shapes[pieces_data[i].index(1)] for i in range(1, 6)]
    active = shapes[pieces_data[6].index(1)]

    if answer[0] == 1:
        action = 'HOLD'
        move = (-1, -1, -1)
    else:
        action = 'MOVE'
        move = (answer[1:11].index(1), answer[11:31].index(1), answer[31:35].index(1))

    return board, hold, queue, active, action, move


data = open('training_data_ultra/game0_example.txt', 'r').read().split('\n')
for i in range(10):
    board, hold, queue, active, action, move = parse_example(data[i])
    print_board(board)
    print('HOLD: ' + hold)
    print('QUEUE: ' + ' '.join(queue))
    print('ACTIVE: ' + active)
    print(action + ' ' + str(move))
