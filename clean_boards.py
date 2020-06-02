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


a = eval(open('replays/game0.txt', 'r').read())
cleaned_boards = []
for (board, preview, queue) in a:
    cleaned_boards.append((clean_board(board), preview, queue))
file = open('replays/game0_cleaned.txt', 'w')
file.write(repr(cleaned_boards))
file.close()

print(cleaned_boards[-1])
