import math

from player import Player


LANE_K: int = 16
GAME_K: int = 10
PLAY_FACTOR: int = 10


# Determines probability to win based on your elo and opponent elo
def probability(elo, opponent_elo):
    return 1 / (1 + (math.pow(10, (opponent_elo - elo) / 400)))


# Determines new elo, based on your laner and other opponents, lane outcome, and game outcome. Lane outcome is valued more.
def new_elo(player: Player, index: int, enemies: list[Player], gold_diff: int, game_outcome: int):
    # calculate win state based on gold diff, 1000 = 1, -1000 = 0, 500 = 0.75, 0 = 0.5
    if gold_diff >= 1000:
        gold_diff = 1
    elif gold_diff <= -1000:
        gold_diff = 0
    else:
        gold_diff = gold_diff/2000 + 0.5
    # calculate elo adjustment based on lane outcome
    lane_elo = LANE_K/math.floor((player.games_played + 1) / PLAY_FACTOR + 1) * (
        gold_diff - probability(player.elo, enemies[index].elo))
    # remove laner after considering it
    enemies.pop(index)
    elo_adjust = 0
    # change rest of elo
    for i in range(4):
        elo_adjust += GAME_K/math.floor(player.games_played/PLAY_FACTOR + 1) * (
            game_outcome - probability(player.elo, enemies[i].elo))
    return round(player.elo + elo_adjust + lane_elo)
