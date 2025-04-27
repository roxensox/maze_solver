from classes import Point, Line, Window, Cell, Maze


def main():
    # y-axis is flipped in game rendering
    win = Window(1920, 1080)
    new_maze = Maze(10, 
                    10,
                    10,
                    10,
                    25,
                    25,
                    win
    )
    win.wait_for_close()



if __name__ == "__main__":
    main()
