import argparse
import json
from rank import Rank
from role import Role

# convert strings into the enums, rank enum might be useless...
ranks: dict = {
    "low iron": Rank.LOW_IRON,
    "high iron": Rank.HIGH_IRON,
    "low bronze": Rank.LOW_BRONZE,
    "high bronze": Rank.HIGH_BRONZE,
    "low silver": Rank.LOW_SILVER,
    "high silver": Rank.HIGH_SILVER,
    "low gold": Rank.LOW_GOLD,
    "high gold": Rank.HIGH_GOLD,
    "low plat": Rank.LOW_PLAT,
    "high plat": Rank.HIGH_PLAT,
    "low emerald": Rank.LOW_EMERALD,
    "high emerald": Rank.HIGH_EMERALD,
    "low diamond": Rank.LOW_DIAMOND,
    "high diamond": Rank.HIGH_DIAMOND,
    "master": Rank.MASTER,
    "grandmaster": Rank.GRANDMASTER,
    "challenger": Rank.CHALLENGER
}

role_options: dict = {
    "top": Role.TOP,
    "jg": Role.JG,
    "mid": Role.MID,
    "adc": Role.BOT,
    "bot": Role.BOT,
    "sup": Role.SUP,
    "fill": Role.FILL,
    "not top": Role.NOT_TOP,
    "not jg": Role.NOT_JG,
    "not mid": Role.NOT_MID,
    "not bot": Role.NOT_BOT,
    "not adc": Role.NOT_BOT,
    "not sup": Role.NOT_SUP
}

# allow list of strings for parsing


def list_of_strings(arg):
    return arg.split(', ')


parser = argparse.ArgumentParser()

parser.add_argument('--name', type=str, required=True)
parser.add_argument('--rank', type=str, required=True)
parser.add_argument('--roles', type=list_of_strings, required=True)

args = parser.parse_args()

name: str = args.name
rank: Rank = ranks[args.rank.lower()]
roles: list[Role] = []
for entry in args.roles:
    # fill is a list, so extend is used rather then append
    try:
        roles.append(role_options[entry])
    except:
        pass

role_names = []
for entry in roles:
    role_names.append(entry.name)

# package data for json
data = {
    "name": name,
    "rank": rank.name,
    "roles": role_names,
    "games_played": 0,
    "elo": rank.value
}

# append to json file
with open("player_info.json", "r+") as file:
    file_data = json.load(file)
    players = file_data["players"]
    for player in players:
        if player["name"] == data["name"]:
            raise Exception("Player already included")
    file_data["players"].append(data)
    file.seek(0)
    json.dump(file_data, file, indent=4)

print("Added to Json File!")  # no real error checking tbh
