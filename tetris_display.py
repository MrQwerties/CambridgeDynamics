from tkinter import *
from tetris_board import *
import random
from tetris_lookahead import possible_locations


class TetrisDisplay(Frame):
    pieces = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')

    def __init__(self, width=10, height=21, shape=None):
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

        self.queue = list(TetrisDisplay.pieces)
        random.shuffle(self.queue)
        self.activePiece = None
        self.spawn_piece()

        self.master.bind('<Left>', lambda _: self.move_active(-1, 0))
        self.master.bind('<Right>', lambda _: self.move_active(1, 0))
        self.master.bind('<Up>', lambda _: self.move_active(0, 1))
        self.master.bind('<Down>', lambda _: self.move_active(0, -1))

        self.master.bind('x', lambda _: self.rotate_active(1))
        self.master.bind('z', lambda _: self.rotate_active(-1))

        self.master.bind('<space>', lambda _: self.place_active())

        self.master.bind('a', lambda _: self.show_possible())

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

        if self.activePiece:
            for (x, y) in self.activePiece.get_blocks():
                self.buttons[x][y].configure(bg='gray')

    def move_active(self, x_move, y_move):
        """ move_active(int x_move, int y_move) -> bool
        Attempts to move the active piece by the given amount.
        Returns True if movement successful and False if movement fails. """
        result = self.activePiece.move(x_move, y_move, self.board)
        self.draw_update()
        return result

    def rotate_active(self, rotate):
        """ rotate_active(int rotate) -> bool
        Attempts to rotate the active piece by the given amount.
        Returns True if rotation successful and False if movement fails. """
        result = self.activePiece.rotate((self.activePiece.state + rotate)%4, self.board)
        self.draw_update()
        return result

    def place_active(self):
        """ place_active()
        Locks in the active piece and spawns a new one.
        Checks if any rows have been cleared. """
        self.board.piece_add(self.activePiece)
        self.board.check_clear()
        self.spawn_piece()
        self.draw_update()

    def spawn_piece(self):
        """ spawn_piece() -> char
        Spawns a new piece using the 7-bag algorithm at the top of the screen.
        Returns the type of piece spawned. """
        if self.shape:
            self.activePiece = TetrisPiece(self.shape, 4, 19, 0)
        else:
            self.activePiece = TetrisPiece(self.queue.pop(0), 5, 18, 0)
            if len(self.queue) < 7:
                new_pieces = list(TetrisDisplay.pieces)
                random.shuffle(new_pieces)
                self.queue += new_pieces

    def show_possible(self):
        shape = self.activePiece.shape
        poss = possible_locations(self.activePiece, self.board)
        print(poss)
        print(len(poss))
        for x, y, s, m in poss:
            self.activePiece = TetrisPiece(shape, x, y, s)
            self.draw_update()
            #time.sleep(0.5)


if __name__ == '__main__':
    t = TetrisDisplay(10, 24)
    t.mainloop()
