from classes import Point, Line, Window, Cell


def main():
    # y-axis is flipped in game rendering
    win = Window(800, 600)
    cell1 = Cell(50, 50, 100, 100, win)
    cell2 = Cell(100, 100, 150, 150, win)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    win.wait_for_close()



if __name__ == "__main__":
    main()
