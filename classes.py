from tkinter import Tk, BOTH, Canvas


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
    def __init__(self, x1, y1, x2, y2, win):
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


    def draw(self):
        line_color = "green"
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
