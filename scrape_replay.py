# To-Do List:
# 1) Parse team names from usernames & get rosters - NOT STARTED
# 2) Collect all moves used by Metronome from battle logs to database - DONE
# 3) Connect moves with corresponding type, power, accuracy, etc. - DONE
#   3.1) Add check if move's stats is already recorded in database - DONE
#   3.2) Add check for valid moves - ON HOLD

import re, openpyxl

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

# Send move data to Excel spreadsheet
def transfer_metronome_data(dict, xl_file, sheetname):
    # Load the existing workbook & worksheet
    workbook = openpyxl.load_workbook(xl_file)
    worksheet = workbook[sheetname]
    # Write the dictionary contents to the worksheet
    for key, value in dict.items():
        # Flag to check if the move exists in the worksheet
        move_exists = False  
        # Search for the move in the existing data
        for row_index, row in enumerate(worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, values_only=True), start=2):
            if row[0] == key:
                # Move already exists, increase the count
                move_exists = True
                worksheet.cell(row=row_index, column=2).value += value
                break
        if move_exists == False:
            # Move doesn't exist, add it to the next available row
            next_row = worksheet.max_row + 1
            worksheet[f"A{next_row}"] = key
            worksheet[f"B{next_row}"] = value
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
        num_iterations = 0
        # Check if the move doesn't contains its stats (which start in column C)
        if target_worksheet.cell(row=row_index, column=3).value is None:
            move_name, count = row[0], row[1]
            # Search for the move in the stats worksheet (moves start in column B)
            for stats_row in stats_worksheet.iter_rows(min_row=2, min_col=2, values_only=True):
                num_iterations += 1
                if stats_row[0] == move_name:
                    valid_move = True
                    # Retrieve Type, Category, Power, Accuracy, Generation, Effect stats (columns C-F, H-I)
                    move_stats = stats_row[1:5] + stats_row[6:8]
                    # print(f"{move_name}: {move_stats}")
                    # Update the corresponding cells in the target worksheet
                    target_worksheet.cell(row=row_index, column=2).value = count
                    for col_index, stat in enumerate(move_stats, start=3):  # Start from column C (index 2)
                        target_worksheet.cell(row=row_index, column=col_index).value = stat
                    # Once move is found & stats populated, stop looping through datasheet
                    break
            # print(f"{move_name}: {num_iterations}")
            # if valid_move == False:
            #     # Not a valid move, remove from data
            #     target_worksheet.delete_rows(row_index)
    # Save the target workbook
    target_workbook.save(target_file)
    return

def get_teams_and_roster():
    return

def main():
    battle_log = "battle_logs_test.txt"

    moves = metronome_data(battle_log)
    
    # TEST: Count each move used & total moves used in a battle
    # for move, count in moves.items():
    #     print(f"{move}: {count}")
    # print(f"Keys: {len(moves.keys())}, Values: {sum(moves.values())}")

    # TEST: Check how moves are being transferred between files
    # test_dict = {"Pound": 1, "Fire Punch": 2, "Cut": 1, "Swords Dance": 1, "Scratch": 2, "Fusion Bolt": 1, "Fly": 1}

    transfer_metronome_data(moves, "tournament_statistics.xlsx", "Metronome_Data (2)")
    connect_move_with_stats("pokemon_data_gen5.xlsx", "Move_Data", "tournament_statistics.xlsx", "Metronome_Data (2)")

if __name__ == "__main__":
    main()

