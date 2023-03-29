from hangman import hangman_game, hangman
from pong_game import init_pong_game, handle_events, update_ball_position, check_ball_collision, draw_objects, pong_game
from rock_paper_scissors import rock_paper_scissors
from tic_tac_toe import init_tic_tac_toe_game, draw_board, draw_x, draw_o, check_game_over, tic_tac_toe

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

main ()
