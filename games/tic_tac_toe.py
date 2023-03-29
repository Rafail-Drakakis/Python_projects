import pygame
import sys

#tic_tac_toe.py
def init_tic_tac_toe_game():
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    pygame.display.set_caption("Tic Tac Toe")
    return screen

def draw_board(screen, board):
    BLACK = (0, 0, 0)
    # Draw horizontal lines
    pygame.draw.line(screen, BLACK, (150, 0), (150, 450), 3)
    pygame.draw.line(screen, BLACK, (300, 0), (300, 450), 3)
    # Draw vertical lines
    pygame.draw.line(screen, BLACK, (0, 150), (450, 150), 3)
    pygame.draw.line(screen, BLACK, (0, 300), (450, 300), 3)

    # Draw tokens
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                draw_x(screen, i, j)
            elif board[i][j] == "O":
                draw_o(screen, i, j)

def draw_x(screen, i, j):
    BLACK = (0, 0, 0)
    pygame.draw.line(screen, BLACK, (50 + i * 150, 50 + j * 150), (100 + i * 150, 100 + j * 150), 3)
    pygame.draw.line(screen, BLACK, (50 + i * 150, 100 + j * 150), (100 + i * 150, 50 + j * 150), 3)

def draw_o(screen, i, j):
    BLACK = (0, 0, 0)
    pygame.draw.circle(screen, BLACK, (75 + i * 150, 75 + j * 150), 50, 3)

def check_game_over(board):
    # Check for a winner
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # Check for a draw
    for row in board:
        if None in row:
            return None
    return "D"
  
def tic_tac_toe():
    screen = init_tic_tac_toe_game()
    WHITE = (255, 255, 255)

    # Game state variables
    board = [[None, None, None], [None, None, None], [None, None, None]]
    player_turn = "X"
    game_over = False

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                i = x // 150
                j = y // 150
                if board[i][j] is None:
                    board[i][j] = player_turn
                    if player_turn == "X":
                        player_turn = "O"
                    else:
                        player_turn = "X"

        # Set the background color to white
        screen.fill(WHITE)
        # Draw the game board
        draw_board(screen, board)
        # Check if the game is over
        result = check_game_over(board)
        if result is not None:
            game_over = True
            if result == "D":
                pygame.display.set_caption("Tic Tac Toe - It's a draw!")
            else:
                pygame.display.set_caption(f"Tic Tac Toe - {result} wins!")

        # Update the display
        pygame.display.update()

    # Quit pygame
    pygame.quit()
    sys.exit()
