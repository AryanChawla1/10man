import argparse
import itertools
import json

from player import Player


# Allows to have list of strongs for parsing
def list_of_strings(arg):
    return arg.split(', ')


# returns Player object by filtering JSON file for name
def get_player_by_name(name):
    with open("player_info.json", "r+") as file:
        file_data = json.load(file)
        players = file_data["players"]
        for player in players:
            if name == player["name"]:
                return Player(player["name"], player["roles"], player["games_played"], player["elo"])
        raise Exception("Cannot find player: " + name)


# Checks if player has role matching their assigned role
def check(player: Player, index):
    if len(player.roles) == 5:
        return (0, True)
    for i in range(len(player.roles)):
        if player.roles[i].value == index:
            # The i is for the index of their role, to determine preference, ith preference
            return (i, True)
    return (False,)


# Checks if entire team is satisfied with their role
def check_team_role(players):
    score = 0
    for i in range(len(players)):
        result = check(players[i], i)
        if len(result) == 1:
            return (False,)
        # score is the sume of their preferences
        score += result[0]
    return (score, True)


# return team's elo
def get_elo(players: list[Player]):
    elo = 0
    for player in players:
        elo += player.elo
    return elo


# create teams
def team_creation(players: list[Player]):
    # all permutations, find best one
    possibilities = list(itertools.permutations(players))
    best_score = -1
    index = -1
    for i in range(len(possibilities)):
        # split into two teams, their indices match with the role enum, ex. top = 0
        team_1 = possibilities[i][0:5]
        team_2 = possibilities[i][5:]
        team_1_result = check_team_role(team_1)
        team_2_result = check_team_role(team_2)
        # check if roles are ok (False,) is length 1 tuple, else it's true [Could be very easily optmized]
        if len(team_1_result) != 1 and len(team_2_result) != 1:
            # score is difference in elo + ith preference of every player (starting at 0)
            score = abs(get_elo(team_1) - get_elo(team_2)) + \
                team_1_result[0] + team_2_result[0]
            # get best score
            if score < best_score or best_score == -1:
                best_score = score
                index = i
    # should be fixed to print them as teams side by side
    print(possibilities[index])
    print(score)


parser = argparse.ArgumentParser()

parser.add_argument('--names', type=list_of_strings, required=True)

args = parser.parse_args()

if len(args.names) != 10:
    raise Exception("10 entries needed")

players = []
for name in args.names:
    players.append(get_player_by_name(name))

team_creation(players)
