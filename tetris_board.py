class TetrisPiece:
    """ Represents a 4-block piece in the game of Tetris. """
    blockShapes = {'I': (((-1, 0), (0, 0), (1, 0), (2, 0)),
                         ((1, 1), (1, 0), (1, -1), (1, -2)),
                         ((-1, -1), (0, -1), (1, -1), (2, -1)),
                         ((0, 1), (0, 0), (0, -1), (0, -2))),
                   'J': (((-1, 1), (-1, 0), (0, 0), (1, 0)),
                         ((1, 1), (0, 1), (0, 0), (0, -1)),
                         ((-1, 0), (0, 0), (1, 0), (1, -1)),
                         ((-1, -1), (0, -1), (0, 0), (0, 1))),
                   'L': (((-1, 0), (0, 0), (1, 0), (1, 1)),
                         ((0, 1), (0, 0), (0, -1), (1, -1)),
                         ((-1, -1), (-1, 0), (0, 0), (1, 0)),
                         ((-1, 1), (0, 1), (0, 0), (0, -1))),
                   'O': (((0, 0), (0, 1), (1, 0), (1, 1)),
                         ((0, 0), (0, 1), (1, 0), (1, 1)),
                         ((0, 0), (0, 1), (1, 0), (1, 1)),
                         ((0, 0), (0, 1), (1, 0), (1, 1))),
                   'S': (((-1, 0), (0, 0), (0, 1), (1, 1)),
                         ((0, 1), (0, 0), (1, 0), (1, -1)),
                         ((-1, -1), (0, -1), (0, 0), (1, 0)),
                         ((-1, 1), (-1, 0), (0, 0), (0, -1))),
                   'T': (((0, 0), (-1, 0), (0, 1), (1, 0)),
                         ((0, 0), (0, 1), (1, 0), (0, -1)),
                         ((0, 0), (1, 0), (0, -1), (-1, 0)),
                         ((0, 0), (0, -1), (-1, 0), (0, 1))),
                   'Z': (((-1, 1), (0, 1), (0, 0), (1, 0)),
                         ((1, 1), (1, 0), (0, 0), (0, -1)),
                         ((-1, 0), (0, 0), (0, -1), (1, -1)),
                         ((0, 1), (0, 0), (-1, 0), (-1, -1)))}

    # The series of wall kicks according to the SRS rotation system
    iKicks = {(0, 1): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
              (1, 0): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
              (1, 2): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
              (2, 1): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
              (2, 3): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
              (3, 2): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
              (3, 0): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
              (0, 3): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1))}

    otherKicks = {(0, 1): ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
                  (1, 0): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
                  (1, 2): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
                  (2, 1): ((0, 0), (1, 0), (-1, 1), (0, -2), (1, -2)),
                  (2, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
                  (3, 2): ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
                  (3, 0): ((0, 0), (1, 0), (-1, -1), (0, 2), (1, 2)),
                  (0, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2))}

    def __init__(self, shape, x=0, y=0, state=0):
        """ TetrisPiece(char shape, int x = 0, int y = 0, int state = 0) -> TetrisPiece
        Creates a Tetris piece of the given shape in the given rotation state and position.
        shape should be one of (I, J, L, O, S, T, Z). """
        self.shape = shape
        self.state = state
        self.blocks = TetrisPiece.blockShapes[self.shape.upper()]
        if self.shape.upper() == 'I':
            self.kicks = TetrisPiece.iKicks
        else:
            self.kicks = TetrisPiece.otherKicks
        self.x = x
        self.y = y

    def get_blocks(self):
        """ get_blocks() -> list of 4 (int, int) pairs
        Returns the locations of the 4 blocks in the piece. """
        return [(self.x + b[0], self.y + b[1]) for b in self.blocks[self.state]]

    def rotate(self, new_state, board):
        """ rotate(int new_state, TetrisBoard board) -> bool
        Rotates the block to the new state according to the SRS rotation system, on the given board.
        Returns True if rotation succeeds, and False if rotation fails. """
        old_state = self.state
        wall_kicks = self.kicks[(old_state, new_state)]
        # Set the piece's state to the new state to see where the rotated piece would fit.
        self.state = new_state
        for (kick_x, kick_y) in wall_kicks:
            if board.piece_fits(self, kick_x, kick_y):
                self.x += kick_x
                self.y += kick_y
                return True
        # Reset piece to old state before returning
        self.state = old_state
        return False

    def move(self, x_move, y_move, board):
        """ move(int x_move, int y_move, TetrisBoard board) -> bool
        Attempts to move the piece by the given amount.
        Returns True if movement succeeds, and False if movement fails. """
        if board.piece_fits(self, x_move, y_move):
            self.x += x_move
            self.y += y_move
            return True
        return False

    def soft_drop(self, board, x_move=0, y_move=-1):
        """ soft_drop(TetrisBoard board, int x_move = 0, int y_move = 0) -> int
        Moves the piece in the given direction (default downwards) as long as possible.
        Returns number of tiles dropped. """
        tiles_dropped = 0
        while self.move(x_move, y_move, board):
            tiles_dropped += 1
        return tiles_dropped

    def on_ground(self, board):
        """ on_ground(TetrisBoard board) -> bool
        Returns whether this piece is resting on a block. """
        for b in self.get_blocks():
            if b[1] == 0:
                return True
            # Check the piece directly below each block
            if board.on_board(b[0], b[1] - 1) and board.board[b[0]][b[1] - 1]:
                return True
        return False


class TetrisBoard:
    """ Represents the grid in a game of Tetris. """
    def __init__(self, width, height):
        """ TetrisBoard(int width, int height) -> TetrisBoard
        A TetrisBoard object with the given width and height. """
        # self.board[i][j] is the ith column (left to right) in the jth row (bottom to top)
        self.board = [[False]*height for _ in range(width)]
        self.width = width
        self.height = height

    def on_board(self, x, y):
        """ on_board(int x, int y) -> bool
        Returns if the location (x, y) is actually a valid location on the board. """
        return (0 <= y < self.height) and (0 <= x < self.width)

    def piece_fits(self, piece, x_offset=0, y_offset=0):
        """ piece_fits(TetrisPiece piece, int x_offset = 0, int y_offset = 0) -> bool
        Determines if the given Tetris piece will fit on the board at (x, y). """
        for b in piece.get_blocks():
            if not self.on_board(b[0] + x_offset, b[1] + y_offset) or self.board[b[0] + x_offset][b[1] + y_offset]:
                return False
        return True

    def piece_add(self, piece):
        """ piece_add(TetrisPiece piece)
        Adds the given piece into the board. """
        for b in piece.get_blocks():
            if self.on_board(b[0], b[1]):
                self.board[b[0]][b[1]] = True

    def clear_row(self, row):
        """ clear_row(int row)
        Clears the given row of the board. """
        for i in range(self.width):
            del(self.board[i][row])
            self.board[i].append(False)

    def check_clear(self):
        """ check_clear() -> int
        Checks which rows should be cleared, and clears them.
        Returns number of cleared rows. """
        rows_cleared = 0
        for j in range(self.height - 1, -1, -1):
            clear = True
            for i in range(self.width):
                if not self.board[i][j]:
                    clear = False
                    break
            if clear:
                self.clear_row(j)
        return rows_cleared

    def stack_height(self):
        """ stack_height() -> int
        Returns the height of the highest block on the board. """
        for j in range(self.height - 1, -1, -1):
            for i in range(self.width):
                if self.board[i][j]:
                    return j + 1
        return 0
