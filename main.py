from classes import Point, Line, Window, Cell, Maze


def main():
    # y-axis is flipped in game rendering
    win = Window(800, 600)
    new_maze = Maze(10, 
                    10,
                    4,
                    4,
                    20,
                    20,
                    win
    )
    win.wait_for_close()



if __name__ == "__main__":
    main()
