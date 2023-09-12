import json

from player import Player


# returns Player object by filtering JSON file for name
def get_player_by_name(name):
    with open("player_info.json", "r+") as file:
        file_data = json.load(file)
        players = file_data["players"]
        for player in players:
            if name == player["name"]:
                return Player(player["name"], player["roles"], player["games_played"], player["elo"])
        raise Exception("Cannot find player: " + name)


# update games_played and elo for player in JSON file
def update_player(name, elo):
    with open("player_info.json", "r+") as file:
        file_data = json.load(file)
        players = file_data["players"]
        for i in range(len(players)):
            if name == players[i]["name"]:
                file_data["players"][i]["elo"] = elo
                file_data["players"][i]["games_played"] += 1
                file.seek(0)
                file.truncate()
                json.dump(file_data, file, indent=4)
                return
