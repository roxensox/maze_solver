from tkinter import Tk, BOTH, Canvas
import time, random


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
        self.__win = win
        self.visited = False


    def draw(self, x1, y1, x2, y2):
        line_color = "green"
        empty_color = "#333333"
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        temp_line_color = line_color  if self.has_left_wall else empty_color
        a = Point(self.__x1, self.__y1)
        b = Point(self.__x1, self.__y2)
        line = Line(a, b)
        self.__win.draw_line(line, temp_line_color)
        temp_line_color = line_color if self.has_right_wall else empty_color
        a = Point(self.__x2, self.__y1)
        b = Point(self.__x2, self.__y2)
        line = Line(a, b)
        self.__win.draw_line(line, temp_line_color)
        temp_line_color = line_color if self.has_bottom_wall else empty_color
        a = Point(self.__x1, self.__y2)
        b = Point(self.__x2, self.__y2)
        line = Line(a, b)
        self.__win.draw_line(line, temp_line_color)
        temp_line_color = line_color if self.has_top_wall else empty_color
        a = Point(self.__x1, self.__y1)
        b = Point(self.__x2, self.__y1)
        line = Line(a, b)
        self.__win.draw_line(line, temp_line_color)
        self.__center_point = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)


    def draw_move(self, to_cell, undo=False):
        line_color = "white" if not undo else "red"
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
        win=None,
        seed=None
    ):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None: random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()


    def __create_cells(self):
        for i in range(self.num_cols):
            cell_row = []
            for j in range(self.num_rows):
                cell_row.append(Cell(win=self.win))
            self.cells.append(cell_row)
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.__draw_cell(i, j)


    def __draw_cell(self, i, j):
        if self.win == None:
            return
        cell = self.cells[i][j]
        cell.win = self.win
        y1 = self.y1 + (i * self.cell_size_y)
        x1 = self.x1 + (j * self.cell_size_x)
        y2 = y1 + self.cell_size_y
        x2 = x1 + self.cell_size_x
        cell.draw(x1, y1, x2, y2)
        self.__animate()


    def __break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.num_cols - 1, self.num_rows - 1)


    def __break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0 and not self.cells[i - 1][j].visited: 
                to_visit.append((i - 1, j))
            if i < len(self.cells) - 1 and not self.cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < len(self.cells[i]) - 1 and not self.cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return
            else:
                direction = to_visit[random.randrange(0, len(to_visit))]
                if direction == (i - 1, j):
                    self.cells[i][j].has_top_wall = False
                    self.cells[i - 1][j].has_bottom_wall = False
                if direction == (i + 1, j):
                    self.cells[i][j].has_bottom_wall = False
                    self.cells[i + 1][j].has_top_wall = False
                if direction == (i, j - 1):
                    self.cells[i][j].has_left_wall = False
                    self.cells[i][j - 1].has_right_wall = False
                if direction == (i, j + 1):
                    self.cells[i][j].has_right_wall = False
                    self.cells[i][j + 1].has_left_wall = False
                self.__break_walls_r(*direction)


    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False


    def solve(self):
        return self.__solve_r(0, 0)


    def __solve_r(self, i, j):
        self.__animate()
        self.cells[i][j].visited = True
        if (i, j) == (self.num_cols - 1, self.num_rows - 1):
            return True

        if (
            i > 0 
            and not self.cells[i][j].has_top_wall 
            and not self.cells[i - 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i - 1][j])
            if self.__solve_r(i - 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i - 1][j], undo=True)

        if (
            i < self.num_cols - 1 
            and not self.cells[i][j].has_bottom_wall 
            and not self.cells[i + 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i + 1][j])
            if self.__solve_r(i + 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i + 1][j], undo=True)

        if (
            j > 0 
            and not self.cells[i][j].has_left_wall 
            and not self.cells[i][j - 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j - 1])
            if self.__solve_r(i, j - 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j - 1], undo=True)

        if (
            j < self.num_cols - 1 
            and not self.cells[i][j].has_right_wall 
            and not self.cells[i][j + 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j + 1])
            if self.__solve_r(i, j + 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j + 1], undo=True)
        return False



    def __animate(self):
        self.win.redraw()
        time.sleep(0.05)

