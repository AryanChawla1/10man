import argparse
import itertools
import json

from player import Player
from database_connection import Database

database = Database()

# Allows to have list of strongs for parsing


def list_of_strings(arg):
    return arg.split(', ')


# Checks if player has role matching their assigned role
def check(player: Player, index):
    length = len(player.roles)
    for i in range(length):
        if player.roles[i].value == index:
            # The i is for the index of their role, to determine preference, ith preference
            return (i * 100, True)
        # -1 represents fill
        if player.roles[i].value == -1:
            # check if they have NOT preference after FILL, if so return false instead
            for j in range(i + 1, length):
                if player.roles[j].value - 5 == index:
                    return (False,)
            return (i * 100, True)
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


# deincentivize lane disparity by checking if lane difference is greater than 100, if so add 100 to score
def lane_disparity(team_1_lane: list[Player] | Player, team_2_lane: list[Player] | Player):
    # considers bot lane as a whole
    if isinstance(team_1_lane, tuple):
        if abs(get_elo(team_1_lane) - get_elo(team_2_lane)) > 100:
            # return abs(get_elo(team_1_lane) - get_elo(team_2_lane))
            return 600
        else:
            return 0
    else:
        if abs(team_1_lane.elo - team_2_lane.elo) > 100:
            # return abs(team_1_lane.elo - team_2_lane.elo)
            return 600
        else:
            return 0


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
        # check lane disparities (bot lane considered as a whole)
        lane_score = 0
        for j in range(3):
            lane_score += lane_disparity(team_1[j], team_2[j])
        lane_score += lane_disparity(team_1[3:], team_2[3:])
        # check if roles are ok (False,) is length 1 tuple, else it's true [Could be very easily optmized]
        if len(team_1_result) != 1 and len(team_2_result) != 1:
            # score is difference in elo + ith preference of every player (starting at 0)
            score = abs(get_elo(team_1) - get_elo(team_2)) + \
                team_1_result[0] + team_2_result[0] + lane_score
            # get best score
            if score < best_score or best_score == -1:
                best_score = score
                index = i

    # should be fixed to print them as teams side by side
    print("Team 1")
    for i in range(5):
        print(possibilities[index][i])
    print("Team 2")
    for i in range(5):
        print(possibilities[index][i+5])

    # create teams in game_data for reference for post_game_adjustment
    with open("game_data.json", "r+") as file:
        file_data = json.load(file)
        roles = ["TOP", "JG", "MID", "BOT", "SUP"]
        for i in range(len(roles)):
            file_data[roles[i]] = [possibilities[index]
                                   [i].name, possibilities[index][i+5].name]
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)
        print("Added to json file!")


parser = argparse.ArgumentParser()

parser.add_argument('--names', type=list_of_strings, required=True)

args = parser.parse_args()

if len(args.names) != 10:
    raise Exception("10 entries needed")

players = []
for name in args.names:
    players.append(database.get_player_by_name(name))

team_creation(players)
