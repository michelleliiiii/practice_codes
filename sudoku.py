import random

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

##################################################################### Solve the Board ######################################################################
def print_board(board):
    print ("-------------------------------")
    for i, row in enumerate(board):
        print ("|", end ="")
        for j, value in enumerate(row):
            print(str(value) + "  ", end = "")
            if j % 3 == 2 and j != 8:
                print ("|", end ="")

        print ("|\n")
        if i % 3 == 2:
            print ("-------------------------------")


def find_empty (board):
# find the next empty spot on board
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == 0:
                return (i,j)
    return 0

def find_block (board,loc):
# find the list of elements in the same block as loc
    x, y = loc
    block = []

    for i in range(x-x%3, x-x%3+3):
        for j in range(y-y%3, y-y%3+3):
            block.append(board[i][j])
    return block


def find_number (board, loc, start = 0):
# find the suitable number on board at loc
# loc = (x,y), coordinate
    x, y = loc

# find list of items that is in the same block as (x,y)
    block = find_block (board,loc)

    for i in range(start+1,10):
        if i not in board[x]: # no same number on the same row
            if i not in [board[k][y] for k in range(len(board))]: # no same number on the same column
                if i not in block: # no same number on the same block
                    return i
    return 0


def back_tracking (board, loc, filled = []):
# to find the first possible value at loc
# if can't, recurse to back trace error in previous fillings
# and fill the board with appropriate value

# filled is list of positions that are filled (don't include the current loc)
# loc is the current location that we are looking for

    while True:
        x, y = loc
        num = find_number(board, loc, board[x][y])

        if (num != 0):
            board[x][y] = num
            filled.append(loc)
            return filled
        else:
            if filled != []:
                board[x][y] = 0
                prev_loc = filled.pop()
                back_tracking(board, prev_loc, filled)
            else:
                return filled
        
    
def solve (board):
# find solution for board and then print it

    print("Find the solution of sudoku:")
    print_board(board)

    loc = find_empty(board)
    filled = back_tracking(board, loc)
    loc = find_empty(board)
    while loc != 0:
        filled_temp = back_tracking(board, loc, filled)
        filled = filled_temp
        if filled == []:
            break
        loc = find_empty(board)
    
    if loc == 0:
        print ("Found the solution!")
        print_board(board)
        return board
    else:
        print ("Can't find the solution!")
        return False


def no_print_solve(board):

    loc = find_empty(board)
    filled = back_tracking(board, loc)
    loc = find_empty(board)
    while loc != 0:
        filled_temp = back_tracking(board, loc, filled)
        filled = filled_temp
        if filled == []:
            break
        loc = find_empty(board)
    
    if loc == 0:
        return board
    else:
        return False
    
    

############################################################## Generate Sudoku ##############################################################

def find_random_number (board, loc):
# find the suitable number on board at loc
# loc = (x,y), coordinate
    x, y = loc

# find list of items that is in the same block as (x,y)
    block = block = find_block (board,loc)

    for i in rand([1,2,3,4,5,6,7,8,9]):
        if i not in board[x]: # no same number on the same row
            if i not in [board[k][y] for k in range(len(board))]: # no same number on the same column
                if i not in block: # no same number on the same block
                    return i
    return 0

def rand (list):
    random.shuffle(list)
    return list


def generate_board_solution():
# generate a 9*9 solvable sudoku
# in a very inefficient way (random generation)

    board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]

    while find_empty(board) != 0:
        board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        for i in rand([0,1,2,3,4,5,6,7,8]):
            for j in rand([0,1,2,3,4,5,6,7,8]):
                num = find_random_number(board,(i,j))
                if num != 0:
                    board[i][j] = num

    return board


def generate_board_solution_revised():
# generate a 9*9 solvable sudoku
# use back tracking again

    board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
    filled = []

    for i in rand([0,1,2,3,4,5,6,7,8]):
        for j in rand([0,1,2,3,4,5,6,7,8]):
            num = find_random_number(board,(i,j))
            if num != 0:
                board[i][j] = num
                filled.append((i,j))
            else: 
                back_tracking (board, (i,j), filled)

    return board

def generate_board (num_of_space = 50):
# use the board solution to generate a complete sudoku
# random selection

    board = generate_board_solution_revised()
    sequence = [0,1,2,3,4,5,6,7,8]
    i = 0

    while i < num_of_space:
        i += 1
        board[random.choice(sequence)][random.choice(sequence)] = 0
    
    return board
           


########################################################################### Other Helper Function ########################################################################

def is_Valid (board, loc, num):
# before inserting a num into board at loc, check if the num is valid
# loc = (x,y), coordinate
    x, y = loc
    block = find_block (board,loc)

# find list of items that is in the same block as (x,y)
    if num not in block:
        if num not in board[x]:
            if num not in [board[k][y] for k in range(len(board))]:
                return True
    
    return False


if __name__ == "__main__":
    board = generate_board ()
    solve(board)