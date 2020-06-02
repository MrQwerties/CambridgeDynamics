game = eval(open('replays/game0_cleaned.txt', 'r').read())
states = []
lastQueue = game[0][2]
lastHold = game[0][1]
for (board, hold, queue) in game[1:]:
    if queue != lastQueue:
        states.append((board, hold, queue))
    elif hold != lastHold:
        states.append((board, hold, queue))
    lastQueue = queue
    lastHold = hold

print(states)