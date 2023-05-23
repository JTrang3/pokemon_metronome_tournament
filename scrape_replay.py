# To-Do List:
# 1) Parse team names from usernames & get rosters - DONE
# 2) Collect all moves used by Metronome from battle logs to database - DONE
# 3) Connect moves with corresponding type, power, accuracy, etc. - DONE
#   3.1) Add check if move's stats is already recorded in database - DONE
#   3.2) Add check for valid moves - ON HOLD
# 4) Compile battle stats (defeats, faints, damage, etc.) from battle logs to database - DONE
#   4.1) Record pokemon's "defeats" stat - DONE
#   4.2) Record pokemon's "faints" stat - DONE
#   4.3) Record pokemon's "damage_given" stat - DONE
#   4.4) Record pokemon's "damage_taken" stat - DONE
# 5) Compile team stats (win, lose, match history) from battle logs to databse - IN PROGRESS

import re, openpyxl

# Gather all the moves used by Metronome in the entire battle
def metronome_data(logs):
    # {"move": "# of times used"}
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

# Send move data to Excel spreadsheet
def transfer_metronome_data(dict, xl_file, sheetname):
    # Load the existing workbook & worksheet
    workbook = openpyxl.load_workbook(xl_file)
    worksheet = workbook[sheetname]
    # Add the move and its occurences to the worksheet
    for key, value in dict.items():
        # Flag to check if the move found in the worksheet
        move_found = False  
        # Search for the move in the existing data
        for row_index, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
            if row[0] == key:
                # Move already exists, increase the usage count
                move_found = True
                worksheet.cell(row=row_index, column=2).value += value
                break
        if move_found == False:
            # Move doesn't exist, add it to a new row
            new_row = worksheet.max_row + 1
            worksheet[f"A{new_row}"] = key
            worksheet[f"B{new_row}"] = value
    # Save the workbook
    workbook.save(xl_file)
    return

# Transfer move's stats from move datafile
def connect_move_with_stats(data_file, data_sheetname, target_file, target_sheetname):
    # Load worksheet where move database is
    stats_workbook = openpyxl.load_workbook(data_file)
    stats_worksheet = stats_workbook[data_sheetname]
    # Load worksheet where move data is going to
    target_workbook = openpyxl.load_workbook(target_file)
    target_worksheet = target_workbook[target_sheetname]
    # Iterate over the rows in the target worksheet
    for row_index, row in enumerate(target_worksheet.iter_rows(min_row=2, values_only=True), start=2):
        # Flag to check for valid move
        valid_move = False
        # Check if the move doesn't contains its stats (which start in column C)
        if target_worksheet.cell(row=row_index, column=3).value is None:
            move_name, count = row[0], row[1]
            # Search for the move in the stats worksheet (moves start in column B)
            for stats_row in stats_worksheet.iter_rows(min_row=2, min_col=2, values_only=True):
                if stats_row[0] == move_name:
                    valid_move = True
                    # Retrieve Type, Category, Power, Accuracy, Generation, Effect stats (columns C-F, H-I)
                    move_stats = stats_row[1:5] + stats_row[6:8]
                    # Update the corresponding cells in the target worksheet
                    target_worksheet.cell(row=row_index, column=2).value = count
                    # Add stats starting from column C
                    for col_index, stat in enumerate(move_stats, start=3):
                        target_worksheet.cell(row=row_index, column=col_index).value = stat
                    # Once move is found & stats populated, stop looping through datasheet
                    break
            # if valid_move == False:
            #     # Not a valid move, remove from data
            #     target_worksheet.delete_rows(row_index)
    # Save the target workbook
    target_workbook.save(target_file)
    return

# Initialize dictionary w/ pokemon's team & match data
def get_teams_and_roster(logs):
    # {"pokemon": ["team type", 0, 0, 0, 0, 0]}
    match_scoreboard = {}
    with open(logs, 'r') as file:
        # Read first 4 lines in battle logs for teams
        file_content = "".join(file.readlines()[0:4])
        # Search for team type and rosters using a pattern
        pattern = r"MTN\s+(\w+)'s team:\n([\w\s/]+)\n"
        team_matches = re.findall(pattern, file_content)
        for match in team_matches:
            # Separate team type and roster
            team_type = match[0]
            roster = match[1].split(" / ")
            # Call store_team_data() here later
            for pokemon in roster:
                # Apply roster pokemon to key, type to value
                match_scoreboard[pokemon] = [team_type, 0, 0, 0, 0, 0]
    return match_scoreboard

def get_victor():
    return

# Read through pokemon database & get pokemon's type
def get_pokemon_type(pokemon):
    # Change to parameter later
    workbook = openpyxl.load_workbook("pokemon_data_gen5.xlsx")
    worksheet = workbook["Pokemon_Data"]
    # Search for pokemon in database
    for row_index, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
        if row[1] == pokemon:
            # Pokemon found, combine pokemon's types into a list
            types = [worksheet.cell(row=row_index, column=col_num).value for col_num in range(3,5)]
            return str(types)
    # Pokemon not found
    print("Pokemon not found")

# Determine which method a pokemon faints
def faint_case(pokemon, case_num):
    match case_num:
        case 1:
            print(f"{pokemon}: Residual")
        case 2.1:
            print(f"{pokemon}: Confusion")
        case 2.2:
            print(f"{pokemon}: Recoil/Self-destruct")
        case 3:
            print(f"{pokemon}: Team kill")
        case 4:
            print(f"{pokemon}: Future Sight/Doom Desire")
        case _:
            print(f"{pokemon}: Normal")
    
# Gather battle statistics from the entire battle
def match_data(logs):
    # Scoreboard: {"pokemon": ["team type", "defeats", "faints", "self-faints", "damage given", "damage taken"]}
    match_scoreboard = get_teams_and_roster(logs)
    # Read the contents of the file
    with open(logs, 'r') as file:
        future_attacking, future_faints_score, case_num = [], None, 0
        for line in file:
            # Check who last used Metronome
            if " used " in line:
                current_action = re.search(r"(?:The opposing )?([^ ]+) used ([^!]+)!", line)
                pokemon_attacking, move_used = current_action.group(1), current_action.group(2)
                # print(f"Pokemon: {pokemon_attacking.group(1)}, Move: {pokemon_attacking.group(2)}")
                # SPECIAL CASE: pokemon uses Future Sight/Doom Desire
                if move_used == "Future Sight" or move_used == "Doom Desire":
                    # Store future attack in a list
                    future_attacking.append(pokemon_attacking)
            # POTENTIAL CASE: Future Sight/Doom Desire misses the target
            # Check for damage dealt
            elif "of its health!" in line:
                pokemon_receiving = re.search(r"(?:The opposing )?[(]?([^ ]+) lost (\d+\.?\d*)% of its health!", line).group(1)
                damage = float(re.search(r"(?:The opposing )?[(]?([^ ]+) lost (\d+\.?\d*)% of its health!", line).group(2))
                # print(f"Pokemon: {pokemon_receiving}, Damage: {damage}")
                # Update receiving pokemon's "damage taken" & attacking pokemon's "damage given" stat
                match_scoreboard[pokemon_receiving][5] += damage
                # Check if pokemon hit by Future Sight/Doom Desire
                if "took the Future Sight attack!" in previous_line or "took the Doom Desire attack!" in previous_line:
                    # Take from list of future attacks & remove earliest attack
                    match_scoreboard[future_attacking[0]][4] += damage
                    if "fainted!" in next(line):
                        future_faints_score = future_attacking[0]
                    future_attacking.pop(0)
                # NOTE: Pokemon won't receive "damage given" score if attacking own team
                elif pokemon_attacking[0] != pokemon_receiving[0]:
                    match_scoreboard[pokemon_attacking][4] += damage
            # Check for pokemon fainting
            elif "fainted!" in line:
                pokemon_fainted = re.search(r"(?:The opposing )?([^ ]+) fainted!", line).group(1)
                # Update fainted pokemon's "faints" stat
                match_scoreboard[pokemon_fainted][2] += 1
                # Check who receives "defeats" score for faint
                # CASE 1: Pokemon faints from residual damage (poison/burn)
                if "was hurt by poison!" in previous_line or "was hurt by its burn!" in previous_line:
                    case_num = 1
                    continue
                # CASE 2.1: Pokemon faints from itself (confusion)
                elif "It hurt itself in its confusion!" in previous_line:
                    match_scoreboard[pokemon_fainted][3] += 1
                    case_num = 2.1
                # CASE 2.2: Pokemon faints from itself (recoil/self-destruct)
                elif pokemon_fainted == pokemon_attacking:
                    match_scoreboard[pokemon_fainted][3] += 1
                    case_num = 2.2
                # CASE 3: Pokemon faints from own team member
                elif pokemon_fainted[0] == pokemon_attacking[0]:
                    # Attacking pokemon won't receive "faints" score
                    case_num = 3
                    continue
                # CASE 4: Pokemon faints from Future Sight/Doom Desire
                elif future_faints_score != None:
                    match_scoreboard[future_faints_score][1] += 1
                    future_faints_score = None
                    case_num = 4
                else:
                    # Update attacking pokemon's "defeats" stat
                    match_scoreboard[pokemon_attacking][1] += 1
                    case_num = 0
                # Testing proper faint cases
                # faint_case(pokemon_fainted, case_num)
            # Ignore empty lines in file
            if line.strip() != "":
                previous_line = line
    return match_scoreboard

# Send battle data statistics to Excel spreadsheet
def transfer_match_data(dict, xl_file, sheetname):
    # Load the existing workbook & worksheet
    workbook = openpyxl.load_workbook(xl_file)
    worksheet = workbook[sheetname]
    # Iterate over the key, values of each pokemon in the scoreboard
    for pokemon, scoreboard in dict.items():
        # Flag to check if pokemon already in the worksheet
        pokemon_found = False
        # Search for the pokemon in the worksheet
        for row_index, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
            if row[0] == pokemon:
                # Pokemon found, append the stats to the existing row
                pokemon_found = True
                for col_index, stats in enumerate(scoreboard, start=3):
                    # Ignore "team type" value in dict
                    if col_index != 3:
                        worksheet.cell(row=row_index, column=col_index).value += stats
        if pokemon_found == False:
            # Pokemon not found, add the stats to a new row
            new_row = worksheet.max_row + 1
            worksheet.cell(row=new_row, column=1).value = pokemon
            type = get_pokemon_type(pokemon)
            worksheet.cell(row=new_row, column=2).value = type
            for col_index, stats in enumerate(scoreboard, start=3):
                worksheet.cell(row=new_row, column=col_index).value = stats
    # Save the workbook
    workbook.save(xl_file)
    return

def main():
    battle_log = "battle_logs_test.txt"

    moves = metronome_data(battle_log)
    scoreboard = match_data(battle_log)
    
    # TEST: Count each move used & total moves used in a battle
    # for move, count in moves.items():
    #     print(f"{move}: {count}")
    # print(f"Keys: {len(moves.keys())}, Values: {sum(moves.values())}")

    # TEST: Check how moves are being transferred between files
    # test_dict = {"Pound": 1, "Fire Punch": 2, "Cut": 1, "Swords Dance": 1, "Scratch": 2, "Fusion Bolt": 1, "Fly": 1}

    # TEST: View initial team rosters
    # print(get_teams_and_roster(battle_log))

    # TEST: View complete scoreboard
    # for key, values in scoreboard.items():
    #     print(f"{key}: {values}" )

    transfer_metronome_data(moves, "tournament_statistics.xlsx", "Metronome_Data (2)")
    connect_move_with_stats("pokemon_data_gen5.xlsx", "Move_Data", "tournament_statistics.xlsx", "Metronome_Data (2)")
    transfer_match_data(scoreboard, "tournament_statistics.xlsx", "Pokemon_Data (2)")


if __name__ == "__main__":
    main()

