# List of possible roles
ROLES = ['Citizen', 'Doctor', 'Gangster']

def initialize_players():
    players = []

    # Read players and roles from a file
    with open("Players.txt", "r") as file:
        lines = file.readlines()

        for line in lines:
            username, role = line.strip().split(" ")
            if role not in ROLES:
                raise ValueError("Invalid role detected.")
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
        for index, player in enumerate(players, start=1):
            print(f"{index}. {player['username']}")
    
    elif choice == 2:
        print("Players and roles:")
        for index, player in enumerate(players, start=1):
            print(f"{index}. {player['username']}, Role: {player['role']}")
    
    elif choice == 3:
        print("Lost players:")
        lost_players = [player for player in players if player['lost']]
        
        if lost_players:
            for index, player in enumerate(lost_players, start=1):
                print(f"{index}. {player['username']}")
        else:
            print("No players have lost yet.")
    
    elif choice == 4:
        if last_lost_player:
            index = players.index(last_lost_player) + 1
            print(f"Last lost player: {index}. {last_lost_player['username']}")
        else:
            print("No player has lost yet.")

def night_phase(players):
    print("Night phase begins.")

    # Find the gangster player
    gangster = next((player for player in players if player['role'] == 'Gangster'), None)

    print(f"The gangster is {gangster['username']}.")

    while True:
        try:
            target_player_id = int(input("Select a player ID to lose: "))
            
            if not 1 <= target_player_id <= len(players):
                raise ValueError("Invalid player ID.")
            target_player = players[target_player_id - 1]
            
            if target_player['lost']:
                raise ValueError("Player has already lost.")
            break
        
        except (ValueError, IndexError):
            print("Invalid player ID. Please enter a valid player ID.")

    # Find the doctor player
    doctor = next((player for player in players if player['role'] == 'Doctor'), None)

    while True:
        try:
            save_player_id = int(input("Select a player ID to save: "))
            if not 1 <= save_player_id <= len(players):
                raise ValueError("Invalid player ID.")
            save_player = players[save_player_id - 1]
            if save_player['lost']:
                raise ValueError("Player has already lost.")
            break
        except (ValueError, IndexError):
            print("Invalid player ID. Please enter a valid player ID.")

    if save_player == target_player:
        print("The doctor saved the player. No player loses tonight.")
    else:
        target_player['lost'] = True
        print(f"{target_player['username']} has lost.")

    # Check if the gangster has lost
    if target_player['role'] == 'Gangster' and target_player['lost']:
        print("The gangster is out of the game. Citizens win!")
        return players, gangster, doctor, target_player, save_player

    return players, gangster, doctor, target_player, save_player

def voting_system(players):
    votes = {}

    # Initialize vote count for each player
    for index, player in enumerate(players, start=1):
        if not player['lost']:
            votes[index] = 0

    while True:
        try:
            for index, player in enumerate(players, start=1):
                if not player['lost']:
                    while True:
                        try:
                            vote = int(input(f"{player['username']}, vote for a player ID to leave: "))
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

            # Find the player(s) with the maximum votes
            vote_count = {player_id: count for player_id, count in votes.items() if count == max_votes}
            
            if len(vote_count) == 1:
                winner_id = next(iter(vote_count))
                print(f"{players[winner_id - 1]['username']} has been selected to leave.")
                return winner_id
            else:
                print("There is a tie-break. Repeat voting procedure with the tied players.")
                players = [player for player in players if player['lost'] or players.index(player) + 1 in vote_count]
                votes = {index: 0 for index, _ in enumerate(players, start=1)}
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
                    print(f"{winner['username']} has lost.")
                    return
            else:
                return
        except ValueError as e:
            print(str(e))

def game_flow():
    players = initialize_players()
    last_lost_player = None

    while True:
        print_menu(players, last_lost_player)
        players, gangster, doctor, target_player, save_player = night_phase(players)

        # Check if gangster has lost
        if gangster['lost']:
            print("The gangster is out of the game. Citizens win!")
            break

        day_phase(players)

        # Check if gangster has lost during the day phase
        if gangster['lost']:
            print("The gangster is out of the game. Citizens win!")
            break

        lost_players = [player for player in players if player['lost']]
        
        if len(lost_players) == len(players) - 1:
            winner = next((player for player in players if not player['lost']), None)
            print(f"{winner['username']} is the winner.")
            break
        elif len(lost_players) == len(players):
            print("All players have lost. There is no winner.")
            break
        else:
            last_lost_player = lost_players[-1]