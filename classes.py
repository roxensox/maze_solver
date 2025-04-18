from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas()
        self.__canvas.pack()
        self.__running = False


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()


    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()


    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b


    def draw(self, cnv, fill_color):
        cnv.create_line(
            self.a.x,
            self.a.y,
            self.b.x,
            self.b.y,
            fill = fill_color,
            width = 2
        )


class Cell:
    def __init__(self, win, x1=0, y1=0, x2=0, y2=0):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__center_point = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        self.__win = win


    def draw(self, x1, y1, x2, y2):
        line_color = "green"
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.has_left_wall:
            a = Point(self.__x1, self.__y1)
            b = Point(self.__x1, self.__y2)
            line = Line(a, b)
            self.__win.draw_line(line, line_color)
        if self.has_right_wall:
            a = Point(self.__x2, self.__y1)
            b = Point(self.__x2, self.__y2)
            line = Line(a, b)
            self.__win.draw_line(line, line_color)
        if self.has_bottom_wall:
            a = Point(self.__x1, self.__y2)
            b = Point(self.__x2, self.__y2)
            line = Line(a, b)
            self.__win.draw_line(line, line_color)
        if self.has_top_wall:
            a = Point(self.__x1, self.__y1)
            b = Point(self.__x2, self.__y1)
            line = Line(a, b)
            self.__win.draw_line(line, line_color)


    def draw_move(self, to_cell, undo=False):
        line_color = "red" if not undo else "gray"
        line = Line(self.__center_point, to_cell.__center_point)
        self.__win.draw_line(line, line_color)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self.__cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.__create_cells()

    def __create_cells(self):
        for i in range(self.num_rows):
            cell_row = []
            for j in range(self.num_cols):
                cell_row.append(Cell(self.win))
            self.__cells.append(cell_row)
        for i, row in enumerate(self.__cells):
            for j, col in enumerate(row):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.win == None:
            return
        cell = self.__cells[i][j]
        cell.win = self.win
        y1 = self.y1 + (i * self.cell_size_y)
        x1 = self.x1 + (j * self.cell_size_x)
        y2 = y1 + self.cell_size_y
        x2 = x1 + self.cell_size_x
        cell.draw(x1, y1, x2, y2)
        self.__animate()



    def __animate(self):
        self.win.redraw()
        time.sleep(0.05)

