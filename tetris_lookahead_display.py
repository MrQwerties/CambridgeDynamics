from tkinter import *
from tetris_board import *
import random
from tetris_lookahead import possible_locations


class TetrisLookaheadDisplay(Frame):
    pieces = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')

    def __init__(self, width=10, height=24, shape=None):
        Frame.__init__(self)
        self.grid()

        self.width = width
        self.height = height
        self.buttons = []
        self.shape = shape
        for i in range(self.width):
            self.buttons.append([])
            for j in range(self.height):
                self.buttons[-1].append(Button(self, text="", width=2, height=1, bg='white',
                                               command=lambda p=(i, j): self.toggle_square(p[0], p[1])))
                self.buttons[-1][-1].grid(row=self.height - j, column=i)
        self.board = TetrisBoard(self.width, self.height)

        self.score_button = Button(self, text='Compute', command=self.compute_score)
        self.score_button.grid(row=0, column=0, columnspan=4)
        self.score_label = Label(self, text='0')
        self.score_label.grid(row=0, column=4, columnspan=4)

        self.draw_update()

    def toggle_square(self, x, y):
        """ toggle_square(int x, int y)
        Toggles the square in the position (x, y) for testing purposes. """
        self.board.board[x][y] = not self.board.board[x][y]
        self.draw_update()

    def draw_update(self):
        """ draw_update()
        Draws the placed blocks and and active piece. """
        # Draw the already placed pieces
        for i in range(self.width):
            for j in range(self.height):
                if self.board.board[i][j]:
                    color = 'black'
                else:
                    color = 'white'
                self.buttons[i][j].configure(bg=color)

    def compute_score(self):
        self.score_label['text'] = str(combine_func(self.board))


def column_height(column):
    if True in column:
        return len(column) - 1 - column[::-1].index(True)
    return 0


def column_func(board):
    heights = [column_height(col) for col in board.board]
    return sum((heights[i + 1] - heights[i]) ** 2 for i in range(len(heights) - 1))


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
    return 0.5 * board.stack_height() + num_holes(board) + 0.05 * column_func(board)


if __name__ == '__main__':
    t = TetrisLookaheadDisplay(10, 24)
    t.mainloop()
