# if "trapped in a vortex!" in line:
#     pokemon_trapped = re.search("trapped_pokemon", line)
#     if "[Alakazam's Synchronize]" in previous_line:
#         dict[pokemon_trapped][6] += {"status": re.search("Alakazam", previous_line)}
#     else:
#         dict[pokemon_trapped][6] += {"status": "pokemon_attacking"}

import re

line = "The opposing Heracross clamped down on Dragonite!"
pokemon_name = re.search(r"([^ ]+)!", line).group(1)
prev_line = "[Alakazam's Synchronize]"
line = "The opposing Pinsir was poisoned!"
# pokemon_ability = re.search(r"([^\ ]+)'s ([^\]]+)", line)
# pokemon_ability = re.search(r"(?<=\[)(?:The opposing )?([^ ]+)'s ([^\]]+)", line)

if "was poisoned!" in line:
    ability_status = re.search(r"(?<=\[)(?:The opposing )?([^ ]+)'s ([^\]]+)", prev_line)
    if "'s " in prev_line:
        print(f"{ability_status.group(1)}")

# match_scoreboard = {"Dragonite": ["Dragon", 1, 0, {"Enemy": "Tyranitar"}],
#                     "Tyranitar": ["Rock", 1, 0, {"Enemy": "Metagross"}]
#                     }
# print(f"1. {match_scoreboard}")
# a = match_scoreboard["Dragonite"][3]["Enemy"]
# b = match_scoreboard[match_scoreboard["Dragonite"][3]["Enemy"]][3]["Enemy"]
# print(f"{a}\n{b}")

# The opposing Tyranitar was poisoned! / The opposing Tyranitar was badly poisoned!
# The opposing Tyranitar was burned!

# The opposing Tyranitar was hurt by poison! / The opposing Tyranitar was hurt by its burn!