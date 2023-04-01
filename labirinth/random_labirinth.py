import random
import sys

UP, DOWN, LEFT, RIGHT = range(4)
NONE = -1
T, F = True, False

def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            if num < 1:
                raise ValueError
            return num
        except ValueError:
            print("Wrong input, use only positive integers!\n")

def check_validity(s1, s2):
    if s1 < 3 or s2 < 3:
        print("Invalid size!\n")
        sys.exit()

def up(i, j, lab):
    lab[i-1][j] = ' '
    lab[i-2][j] = ' '
    return i-2, j

def down(i, j, lab):
    lab[i+1][j] = ' '
    lab[i+2][j] = ' '
    return i+2, j

def left(i, j, lab):
    lab[i][j-1] = ' '
    lab[i][j-2] = ' '
    return i, j-2

def right(i, j, lab):
    lab[i][j+1] = ' '
    lab[i][j+2] = ' '
    return i, j+2

def roll(b):
    return random.randrange(b)

def movement(i, j, N, M, lab):
    moves = [NONE] * 4
    options = 0
    
    s1 = N-1 if N % 2 == 0 else N
    s2 = M-1 if M % 2 == 0 else M
    
    can_move_up = i - 2 > 0 and lab[i-1][j] == 'X' and lab[i-2][j] == 'X'
    can_move_down = i + 2 < s1 and lab[i+1][j] == 'X' and lab[i+2][j] == 'X'
    can_move_left = j - 2 > 0 and lab[i][j-1] == 'X' and lab[i][j-2] == 'X'
    can_move_right = j + 2 < s2 and lab[i][j+1] == 'X' and lab[i][j+2] == 'X'
    
    if can_move_up:
        moves[options] = UP
        options += 1
    if can_move_down:
        moves[options] = DOWN
        options += 1
    if can_move_left:
        moves[options] = LEFT
        options += 1
    if can_move_right:
        moves[options] = RIGHT
        options += 1
    
    if options != 0:
        move = moves[roll(options)]
        if move == UP:
            return up(i, j, lab)
        elif move == DOWN:
            return down(i, j, lab)
        elif move == LEFT:
            return left(i, j, lab)
        else:
            return right(i, j, lab)
    else:
        return None

def print_labyrinth(lab):
    for row in lab:
        print(' '.join(row))

def dig(i, j, N, M, lab):
    x, y = i, j
    while True:
        new_pos = movement(x, y, N, M, lab)
        if new_pos is None:
            break
        x, y = new_pos
        dig(x, y, N, M, lab)

def create_labyrinth(N, M):
    lab = [['X' for _ in range(M)] for _ in range(N)]
    lab[0][1] = ' '
    lab[1][1] = ' '
    return lab

def main():
    N = input_number("Enter the size of the first dimension: ") # array[N][]
    M = input_number("Enter the size of the second dimension: ") # array[][M]
    check_validity(N, M)
    lab = create_labyrinth(N, M)
    random.seed()
    dig(1, 1, N, M, lab)
    print_labyrinth(lab)
    
main()
