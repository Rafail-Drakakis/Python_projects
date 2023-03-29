import random
import pygame
import sys

#main.py
def main():
	choice = int(input("Press \n1.To play tic tac toe \n2.To play hangman \n3.To play rock paper scissors \n4.To play the pong game: "))
	if choice == 1:
	    tic_tac_toe()
	elif choice == 2:
	    hangman()
	elif choice == 3:
	    rock_paper_scissors()
	elif choice == 4:
	    pong_game()
    
#hangman.py
def hangman_game(word):
    word = word.lower()
    word_letters = set(word)
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    used_letters = set()
    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print("You have {} lives left".format(lives))
        print("Used letters:", ' '.join(used_letters))
        print("Word: ", end="")
        for letter in word:
            if letter in used_letters:
                print(letter, end=" ")
            else:
                print("_", end=" ")
        print("\n")

        user_letter = input("Enter a letter: ").lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives -= 1
        elif user_letter in used_letters:
            print("You have already used this letter")
        else:
            print("Invalid input")

    if lives == 0:
        print("You lost! The word was {}".format(word))
    else:
        print("Congratulations! You guessed the word {}".format(word))

def hangman():
    words = [
        'hangman', 'chairs', 'backpack', 'desk', 'python', 'laptop',
        'computer', 'programming', 'keyboard', 'television', 'guitar',
        'headphones', 'pencil', 'eraser', 'calculator', 'cactus',
        'flower', 'mug', 'table', 'curtain', 'refrigerator', 'stove',
        'microwave', 'bread', 'butter', 'chocolate', 'sandwich',
        'tomato', 'potato', 'carrot', 'pepper', 'lettuce', 'pumpkin',
        'elephant', 'giraffe', 'kangaroo', 'zebra', 'lion', 'tiger',
        'penguin', 'dolphin', 'whale', 'shark', 'octopus', 'jellyfish',
        'bicycle', 'motorcycle', 'airplane', 'helicopter', 'train',
        'subway', 'ship', 'sailboat', 'skateboard', 'rollerblade'
    ]
    hangman_game(random.choice(words))

#pong_game.py
def init_pong_game():
    pygame.init()
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pong")
    return screen

def handle_events(paddle_1_position, paddle_2_position):
    paddle_speed = 40
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, paddle_1_position, paddle_2_position
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_1_position = max(0, paddle_1_position - paddle_speed)
            elif event.key == pygame.K_s:
                paddle_1_position = min(300, paddle_1_position + paddle_speed)
            elif event.key == pygame.K_UP:
                paddle_2_position = max(0, paddle_2_position - paddle_speed)
            elif event.key == pygame.K_DOWN:
                paddle_2_position = min(300, paddle_2_position + paddle_speed)
    return True, paddle_1_position, paddle_2_position

def update_ball_position(ball_position, ball_speed):
    ball_position[0] += ball_speed[0]
    ball_position[1] += ball_speed[1]
    return ball_position

def check_ball_collision(ball_position, ball_speed, paddle_1_position, paddle_2_position):
    if ball_position[1] < 0 or ball_position[1] > 300:
        ball_speed[1] = -ball_speed[1]
    if ball_position[0] < 0:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 200
        ball_position[1] = 150
    elif ball_position[0] > 400:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 200
        ball_position[1] = 150

    if ball_position[0] < 25 and ball_position[1] > paddle_1_position - 50 and ball_position[1] < paddle_1_position + 50:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 25
    elif ball_position[0] > 375 and ball_position[1] > paddle_2_position - 50 and ball_position[1] < paddle_2_position + 50:
        ball_speed[0] = -ball_speed[0]
        ball_position[0] = 375

    return ball_position, ball_speed

def draw_objects(screen, ball_position, paddle_1_position, paddle_2_position):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, paddle_1_position - 50, 25, 100))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(375, paddle_2_position - 50, 25, 100))
    pygame.draw.circle(screen, (255, 255, 255), ball_position, 10)
    pygame.display.flip()

def pong_game():
    pygame.init()
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pong")

    ball_speed = [2, 2]
    ball_position = [200, 150]
    paddle_1_position = 150
    paddle_2_position = 150

    running = True
    while running:
        running, paddle_1_position, paddle_2_position = handle_events(paddle_1_position, paddle_2_position)
        ball_position = update_ball_position(ball_position, ball_speed)
        ball_position, ball_speed = check_ball_collision(ball_position, ball_speed, paddle_1_position, paddle_2_position)
        draw_objects(screen, ball_position, paddle_1_position, paddle_2_position)
        pygame.time.delay(10)

    pygame.quit()
    
#rock_paper_scissors.py
def rock_paper_scissors():
  # Create a list of play options
  plays = ["rock", "paper", "scissors"]

  # Display instructions
  print("Enter a play: rock, paper, or scissors")

  # Get the player's play
  player_play = input().lower()

  # Check that the player's play is valid
  if player_play not in plays:
    print("Invalid play. Please enter rock, paper, or scissors.")
    pass

  # Have the computer choose a play at random
  computer_play = random.choice(plays)

  # Display the plays
  print(f"You played {player_play}. The computer played {computer_play}.")

  # Determine the winner
  if player_play == computer_play:
    print("It's a tie!")
  elif (player_play == "rock" and computer_play == "scissors") or (player_play == "paper" and computer_play == "rock") or (player_play == "scissors" and computer_play == "paper"):
    print("You win!")
  else:
    print("The computer wins!")
    
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
    
main()
