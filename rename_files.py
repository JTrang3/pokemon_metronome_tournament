import os
import re

main_folder_name = input("Select folder: ")
main_folder_path = os.path.join(os.getcwd(), main_folder_name)
# Define the regex pattern to extract the desired groups
pattern = r"Gen5TriplesCustomGame-\d{4}-\d{2}-\d{2}-mtn(\w+)-mtn(\w+)(?: \((\d+)\))?\.html"
# Iterate over the subfolders within the main folder
for folder_name in os.listdir(main_folder_path):
    sub_folder_path = os.path.join(main_folder_path, folder_name)
    if os.path.isdir(sub_folder_path):
        # Iterate over the files in the folder
        for file_name in os.listdir(sub_folder_path):
            file_path = os.path.join(sub_folder_path, file_name)
            if os.path.isfile(file_path):
                # Match the regex pattern against the filename
                match = re.match(pattern, file_name)
                if match:
                    # Extract the groups
                    group1 = match.group(1)
                    group2 = match.group(2)
                    group3 = int(match.group(3)) + 1 if match.group(3) else 1
                    # Construct the new filename
                    new_filename = f"{folder_name}-{group1}-{group2}-g{group3}.html"
                    new_file_path = os.path.join(sub_folder_path, new_filename)
                    # Rename the file
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{file_name}' to '{new_filename}'")
                else:
                    print(f"Skipped '{file_name}' as it doesn't match the pattern.")