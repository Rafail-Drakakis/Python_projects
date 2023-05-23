import random

ROLES = ['Citizen', 'Doctor', 'Gangster']

class Round:
    def __init__(self, players, gangster, doctor, target_player, save_player, lost_player=None):
        self.players = players
        self.gangster = gangster
        self.doctor = doctor
        self.target_player = target_player
        self.save_player = save_player
        self.lost_player = lost_player

    def __str__(self):
        return f"Players: {', '.join(player['username'] for player in self.players)}\n" \
               f"Gangster: {self.gangster['username']}\n" \
               f"Doctor: {self.doctor['username']}\n" \
               f"Target player: {self.target_player['username']}\n" \
               f"Save player: {self.save_player['username']}\n" \
               f"Lost player: {self.lost_player['username'] if self.lost_player else 'None'}\n"

def initialize_players():
    players = []

    with open("Players.txt", "r") as file:
        lines = file.readlines()

        for line in lines:
            username, role = line.strip().split(" ")
            players.append({'username': username, 'role': role, 'lost': False})

    return players

def print_menu(players, last_lost_player):
    print("----- Info Menu -----")
    print("1. Print all players")
    print("2. Print players and roles")
    print("3. Print lost players")
    print("4. Print last lost player")
    print("---------------------")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > 4:
                raise ValueError()
            break
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 4.")

    if choice == 1:
        print("All players:")
        for player in players:
            print(f"Player ID: {players.index(player) + 1}, Username: {player['username']}")
    elif choice == 2:
        print("Players and roles:")
        for player in players:
            print(f"Player ID: {players.index(player) + 1}, Username: {player['username']}, Role: {player['role']}")
    elif choice == 3:
        print("Lost players:")
        lost_players = [player for player in players if player['lost']]
        if lost_players:
            for player in lost_players:
                print(f"Player ID: {players.index(player) + 1}, Username: {player['username']}")
        else:
            print("No players have lost yet.")
    elif choice == 4:
        if last_lost_player:
            print(f"Last lost player: Player ID: {players.index(last_lost_player) + 1}, Username: {last_lost_player['username']}")
        else:
            print("No player has lost yet.")

def night_phase(players):
    print("Night phase begins.")

    gangster = next((player for player in players if player['role'] == 'Gangster'), None)

    print(f"The gangster is Username: {gangster['username']}.")

    while True:
        try:
            target_player_id = int(input("Select a player ID to lose: "))
            target_player = players[target_player_id - 1]
            if target_player['lost']:
                raise ValueError("Player has already lost.")
            break
        except (ValueError, IndexError):
            print("Invalid player ID.")

    doctor = next((player for player in players if player['role'] == 'Doctor'), None)

    while True:
        try:
            save_player_id = int(input("Select a player ID to save: "))
            save_player = players[save_player_id - 1]
            if save_player['lost']:
                raise ValueError("Player has already lost.")
            break
        except (ValueError, IndexError):
            print("Invalid player ID.")

    if save_player == target_player:
        print("The doctor saved the player. No player loses tonight.")
    else:
        target_player['lost'] = True
        print(f"Player ID: {target_player_id}, Username: {target_player['username']} has lost.")

    return Round(players, gangster, doctor, target_player, save_player)

def voting_system(players):
    votes = {}

    for i, player in enumerate(players):
        if not player['lost']:
            votes[i + 1] = 0

    while True:
        try:
            for i, player in enumerate(players):
                if not player['lost']:
                    while True:
                        try:
                            vote = int(input(f"Player ID: {i + 1}, Username: {player['username']}, vote for a player ID to leave: "))
                            if vote in votes:
                                break
                            else:
                                raise ValueError("Invalid vote.")
                        except ValueError:
                            print("Invalid vote. Please enter a valid player ID.")

                    votes[vote] += 1

            max_votes = max(votes.values())
            if max_votes == 0:
                print("No votes were cast. Voting procedure ends without a 'winner'.")
                return None

            vote_count = {player_id: count for player_id, count in votes.items() if count == max_votes}
            if len(vote_count) == 1:
                winner_id = next(iter(vote_count))
                print(f"Player ID: {winner_id} has been selected to leave.")
                return winner_id
            else:
                print("There is a tie-break. Repeat voting procedure with the tied players.")
                players = [player for player in players if player['player_id'] in vote_count]
                votes = {i + 1: 0 for i, _ in enumerate(players)}
        except ValueError as e:
            print(str(e))
            votes = {}

def day_phase(players):
    print("Day phase begins.")

    while True:
        try:
            winner_id = voting_system(players)
            if winner_id:
                winner = next((player for player in players if players.index(player) + 1 == winner_id), None)
                if winner:
                    winner['lost'] = True
                    print(f"Player ID: {winner_id}, Username: {winner['username']} has lost.")
                    return
            else:
                return
        except ValueError as e:
            print(str(e))

def game_flow():
    players = initialize_players()
    last_lost_player = None
    rounds = []

    while True:
        print_menu(players, last_lost_player)
        round_info = night_phase(players)
        rounds.append(round_info)

        if next((player for player in players if player['role'] == 'Gangster' and player['lost']), None):
            print("The gangster has lost. Citizens win!")
            break

        day_phase(players)

        lost_players = [player for player in players if player['lost']]
        if len(lost_players) == len(players) - 1:
            winner = next((player for player in players if not player['lost']), None)
            print(f"Player ID: {players.index(winner) + 1}, Username: {winner['username']} is the winner.")
            break
        elif len(lost_players) == len(players):
            print("All players have lost. There is no winner.")
            break
        else:
            last_lost_player = lost_players[-1]

    with open("TownOfSalem_output.txt", "w") as file:
        for i, round_info in enumerate(rounds):
            file.write(f"Round {i + 1}:\n{str(round_info)}\n")