# To-Do List:
# 1) Parse team names from usernames & get rosters - NOT STARTED
# 2) Collect all moves used by Metronome from battle logs to database - DONE
# 3) Connect moves with corresponding type, power, accuracy (include priority & description?) - IN PROGRESS

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
    # row = worksheet.max_row + 1
    # for key, value in dict.items():
    #     worksheet[f"A{row}"] = key
    #     worksheet[f"B{row}"] = value
    #     row += 1
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

def get_teams_and_roster():
    return

def main():
    battle_log = "battle_logs_test.txt"

    moves = metronome_data(battle_log)
    
    # TEST: Count each move used & total moves used in a battle
    # for move, count in moves.items():
    #     print(f"{move}: {count}")
    # print(f"Keys: {len(moves.keys())}, Values: {sum(moves.values())}")

    transfer_metronome_data(moves, "tournament_statistics.xlsx", "Metronome_Data (2)")

if __name__ == "__main__":
    main()

