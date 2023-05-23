import random

#rock_paper_scissors.py
def rock_paper_scissors():
  # Create a list of play options
  plays = ["rock", "paper", "scissors"]

  # Display instructions
  print("Enter a play: rock, paper, or scissors")
  
  while True:
    # Get the player's play
    player_play = input().lower()

    # Check that the player's play is valid
    if player_play not in plays:
        print("Invalid play. Please enter rock, paper, or scissors.")
    else:
        break

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

