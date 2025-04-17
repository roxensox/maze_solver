from classes import Point, Line, Window, Cell


def main():
    # y-axis is flipped in game rendering
    cell = Cell(100, 100, 200, 200)
    win = Window(800, 600)
    cell.draw(win)
    win.wait_for_close()



if __name__ == "__main__":
    main()
