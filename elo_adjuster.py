import math

LANE_K = 16
GAME_K = 10
PLAY_FACTOR = 10


# Determines probability to win based on your elo and opponent elo
def probability(elo, opponent_elo):
    return 1 / (1 + (math.pow(10, (opponent_elo - elo) / 400)))


# Determines new elo, based on your laner and other opponents, lane outcome, and game outcome. Lane outcome is valued more.
def new_elo(player: object, lane_elo, elo_1, elo_2, elo_3, elo_4, lane_outcome, game_outcome):
    return round(player.elo +
                 LANE_K/math.floor(player.games_played/PLAY_FACTOR + 1)(lane_outcome - probability(player.elo, lane_elo)) +
                 GAME_K/math.floor(player.games_played/PLAY_FACTOR + 1)(game_outcome - probability(player.elo, elo_1)) +
                 GAME_K/math.floor(player.games_played/PLAY_FACTOR + 1)(game_outcome - probability(player.elo, elo_2)) +
                 GAME_K/math.floor(player.games_played/PLAY_FACTOR + 1)(game_outcome - probability(player.elo, elo_3)) +
                 GAME_K/math.floor(player.games_played/PLAY_FACTOR + 1)(game_outcome - probability(player.elo, elo_4)))
