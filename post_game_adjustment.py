import argparse
import json

from elo_adjuster import *
from player import Player
from database_connection import *


# Allows to have list of strongs for parsing
def list_of_strings(arg):
    return arg.split(', ')


parser = argparse.ArgumentParser()

parser.add_argument('--results', type=list_of_strings, required=True)

args = parser.parse_args()

# which team won (1 or 2), and gold difference between team 1 and 2 for every lane (+500 means team 1 + 500 = team 2)
if len(args.results) != 6:
    raise Exception("6 entries needed")

# convert to int
results = [eval(i) for i in args.results]

# get players from game_data.json
with open("game_data.json", "r+") as file:
    file_data = json.load(file)
    roles = ["TOP", "JG", "MID", "BOT", "SUP"]
    team_1: list[Player] = []
    team_2: list[Player] = []
    new_elo_1 = []
    new_elo_2 = []
    for i in range(len(roles)):
        team_1.append(get_player_by_name(file_data[roles[i]][0]))
        team_2.append(get_player_by_name(file_data[roles[i]][1]))
# get the new elos
for i in range(5):
    new_elo_1.append(
        new_elo(team_1[i], i, team_2[:], results[i + 1], results[0] % 2))
    print(team_1[i].name + ": " + str(team_1[i].elo) +
          " -> " + str(new_elo_1[i]))
    new_elo_2.append(
        new_elo(team_2[i], i, team_1[:], -1 * results[i + 1], results[0] - 1))
    print(team_2[i].name + ": " + str(team_2[i].elo) +
          " -> " + str(new_elo_2[i]))

# update the players
for i in range(5):
    update_player(team_1[i].name, new_elo_1[i])
    update_player(team_2[i].name, new_elo_2[i])
