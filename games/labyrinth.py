import random
import sys

UP, DOWN, LEFT, RIGHT = range(4)

def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            if num < 1:
                raise ValueError
            return num
        except ValueError:
            print("Wrong input, use only positive integers!\n")

def create_labyrinth(n, m):
    labyrinth = [['X' for _ in range(m)] for _ in range(n)]
    labyrinth[0][1] = ' '
    labyrinth[1][1] = ' '
    return labyrinth

def check_validity(n, m):
    if n < 3 or m < 3:
        print("Invalid size!\n")
        sys.exit()

def move(i, j, labyrinth, direction):
    if direction == UP:
        labyrinth[i-1][j] = ' '
        labyrinth[i-2][j] = ' '
        return i-2, j
    elif direction == DOWN:
        labyrinth[i+1][j] = ' '
        labyrinth[i+2][j] = ' '
        return i+2, j
    elif direction == LEFT:
        labyrinth[i][j-1] = ' '
        labyrinth[i][j-2] = ' '
        return i, j-2
    elif direction == RIGHT:
        labyrinth[i][j+1] = ' '
        labyrinth[i][j+2] = ' '
        return i, j+2

def roll(die):
    return random.randrange(die)

def valid_move(i, j, labyrinth, direction):
    if direction == UP:
        return i - 2 > 0 and labyrinth[i-1][j] == 'X' and labyrinth[i-2][j] == 'X'
    elif direction == DOWN:
        return i + 2 < len(labyrinth)-1 and labyrinth[i+1][j] == 'X' and labyrinth[i+2][j] == 'X'
    elif direction == LEFT:
        return j - 2 > 0 and labyrinth[i][j-1] == 'X' and labyrinth[i][j-2] == 'X'
    elif direction == RIGHT:
        return j + 2 < len(labyrinth[0])-1 and labyrinth[i][j+1] == 'X' and labyrinth[i][j+2] == 'X'
    else:
        return False

def movement(i, j, labyrinth):
    moves = []
    for direction in [UP, DOWN, LEFT, RIGHT]:
        if valid_move(i, j, labyrinth, direction):
            moves.append(direction)
    if moves:
        direction = moves[roll(len(moves))]
        return move(i, j, labyrinth, direction)
    else:
        return None

def dig(i, j, labyrinth):
    new_pos = (i, j)
    while new_pos:
        new_pos = movement(i, j, labyrinth)
        if new_pos:
            i, j = new_pos

def print_labyrinth(labyrinth):
    for row in labyrinth:
        print(' '.join(row))

def labyrinth():
    n = input_number("Enter the size of the first dimension: ")
    m = input_number("Enter the size of the second dimension: ")
    check_validity(n, m)
    labyrinth = create_labyrinth(n, m)
    random.seed()
    dig(1, 1, labyrinth)
    print_labyrinth(labyrinth)
