from tkinter import *
import numpy as np
from PIL import ImageGrab


class TetrisScreenGrabDisplay(Frame):
    colors = {'#0f9bd7': 'I', '#2141c6': 'J', '#e35b02': 'L', '#e39f02': 'O',
              '#59b101': 'S', '#af298a': 'T', '#d70f37': 'Z', '#a6a6a6': 'X'}

    def __init__(self, width=10, height=20):
        Frame.__init__(self)
        self.grid()

        self.x0 = 15
        self.y0 = 585
        self.squareSize = 30

        self.width = width
        self.height = height
        self.buttons = []
        for i in range(self.width):
            self.buttons.append([])
            for j in range(self.height):
                self.buttons[-1].append(Button(self, text="", width=2, height=1, bg='blue',
                                               command=lambda p=(i, j): self.get_color(p[0], p[1])))
                self.buttons[-1][-1].grid(row=self.height - j, column=i)

        self.draw_update()

    def draw_update(self):
        """ draw_update()
        Makes a board corresponding to the one on screen. """
        screenshot = np.array(ImageGrab.grab(bbox=(490, 218, 910, 812)))
        for i in range(self.width):
            for j in range(self.height):
                if self.square_color(i, j, screenshot) in TetrisScreenGrabDisplay.colors.keys():
                    self.buttons[i][j].configure(bg='black')
                else:
                    self.buttons[i][j].configure(bg='white')
                self.buttons[i][j].configure(bg=self.square_color(i, j, screenshot))
        self.master.after(100, self.draw_update)

    def get_color(self, x, y):
        print(self.buttons[x][y].cget('bg'))

    def square_color(self, x, y, screenshot):
        """ square_color(int x, int y, 2D array screenshot) -> RGB color string
        Returns the rgb color string of the square in the position (x, y), based on the screenshot. """
        r, g, b = screenshot[self.y0 - self.squareSize * y][self.x0 + self.squareSize * x]
        #print(r, g, b)
        return '#' + hex(65536 * r + 256 * g + b)[2:].zfill(6)


test = TetrisScreenGrabDisplay()
test.mainloop()
