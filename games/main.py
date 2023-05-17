from hangman import hangman
from pong_game import pong_game
from rock_paper_scissors import rock_paper_scissors
from tic_tac_toe import tic_tac_toe
from labyrinth import labyrinth

def main():
    choice = int(input("Press \n1.To play tic tac toe \n2.To play hangman \n3.To play rock paper scissors \n4.To play the pong game \n5.To generate a random labyrinth: "))
    if choice == 1:
        tic_tac_toe()
    elif choice == 2:
        hangman()
    elif choice == 3:
        rock_paper_scissors()
    elif choice == 4:
        pong_game()
    elif choice == 5:
        labyrinth()
    else:
    	print ("Invalid input! ")

main()