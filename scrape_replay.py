# To-Do List:
# 1) Parse team names from usernames & get rosters - NOT STARTED
# 2) Collect all moves used by Metronome from battle logs to database - IN PROGRESS

import re

# Gather all the moves used by Metronome in the entire battle
def metronome_data(logs):
    moves_used = {}
    # Open the file in read mode
    with open(logs, "r") as file:
        # Read the entire content of the file
        file_content = file.read()
        # Search for move occurrences using a pattern
        pattern = r"Waggling a finger let it use (.*?)!"
        move_matches = re.findall(pattern, file_content)
        # Count the moves and store in the dictionary
        for move in move_matches:
            moves_used[move] = moves_used.get(move, 0) + 1
    return moves_used

def get_teams_and_roster():
    return

def main():
    battle_log = "battle_logs_test.txt"

    moves = metronome_data(battle_log)
    
    # TEST: Count each move used & total moves used in a battle
    for move, count in moves.items():
        print(f"{move}: {count}")
    print(f"Keys: {len(moves.keys())}, Values: {sum(moves.values())}")

if __name__ == "__main__":
    main()

