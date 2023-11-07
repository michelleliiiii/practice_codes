'''
The function "find_path" receives a 2D maze where "#" are walls, "O" is the entrance, and "X" is the exit.
It will print out every step the code takes to find the path between "O" and "X".
'''

import curses
from curses import wrapper
import queue
import time


maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze (maze, stdscr, path = []):
    BLUE = curses.color_pair (1)
    RED = curses.color_pair (2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr (i*2, j*4, "*", RED)
            else:
                stdscr.addstr (i*2, j*4, value, BLUE)


def main (stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path (maze, stdscr)
    stdscr.getch()


def find_next_step (maze, visited, q, stdscr):
    # function: take current location out, put next step into queue, return all the locations put into queue
    # maze is a 2D list
    # location as a tuple of coordinates
    # visited as a list of tuples with visited coordinates\

    next_step = []
    new_path = []
    location, path = q.get() # push previous point out of queue

    # use four repeated statement to check four different directions
    # up
    if location[0] > 0 and maze[location[0]-1][location[1]] != "#" and ((location[0]-1, location[1]) not in path):
        # if next step up == unvisited path
        next_step.append((location[0]-1, location[1]))
    # down
    if location[0] < len(maze) and maze[location[0]+1][location[1]] != "#" and ((location[0]+1, location[1]) not in path):
        next_step.append((location[0]+1, location[1]))
    # left
    if location[1] > 0 and maze[location[0]][location[1]-1] != "#" and ((location[0], location[1]-1) not in path):
        next_step.append((location[0], location[1]-1))
    # right
    if location[1] < len(maze) and maze[location[0]][location[1]+1] != "#" and ((location[0], location[1]+1) not in path):
        next_step.append((location[0], location[1]+1))

    for new_location in next_step:
        new_path = path + [new_location]
        q.put ((new_location, new_path))

        stdscr.clear()
        print_maze (maze, stdscr, new_path)
        time.sleep (0.5)
        stdscr.refresh()

    visited.append(next_step)
    return next_step


def find_path (maze, stdscr):
    # get a list of location that form the shortest path from start to end

    # build a queue
    q = queue.Queue()
    visited = []

    # find start and end
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == "O":
                start = (i,j)
            elif value == "X":
                end = (i,j)

    # put starting point into queue
    q.put ((start, [start]))
    visited.append(start)

    # find next steps
    next_step = find_next_step (maze, visited, q, stdscr) 

    while not (q.empty() or next_step == []):
        next_step_temp = []
        for i in next_step:
            new = find_next_step (maze, visited, q, stdscr)
            next_step_temp += new
            if end in new:
                print ("looking for exit")
                for next in new:
                    next = q.get()
                    if next[0] == end:
                        stdscr.clear()
                        print_maze (maze, stdscr, next[1])
                        print("You find the exit!")
                        return next[1]
                    
        next_step = next_step_temp

        if end in next_step:
            print ("looking for exit")
            for next in next_step:
                next = q.get()
                if next[0] == end:
                    stdscr.clear()
                    print_maze (maze, stdscr, next[1])
                    print("You find the exit!")
                    return next[1]
            
    


print ("Welcome to the maze!")
time.sleep(1)
wrapper(main)
