# League 10 Man Team Creator

## Description

Elo-based system that can create balanced teams based on player info.

## Using Project

- Create a venv using:

```
python -m venv .\venv
```

- Activate venv:

```
.\venv\Scripts\activate
```

- Get required modules/dependencies:

```
pip install -r requirements.txt
```

## Tools

### Player Creation

Create players using `player_creator.py`. Make sure to include `--name`, `--rank`, and `--roles`. Rank must be low/high of rank, with the exception of master, grandmater and challenger. Role should be prioritized; `fill` can be used for all roles. More details about fill can be found below.
Created player will start off with elo solely considering the rank, however, as games continue, a proper elo will be calculated based on performance and lane performance.

#### Fill Design

The problem with fill is that player can still have preference for roles. For example, a player can play every role, but have a preference for all 5 roles: top, mid, adc, jg sup. You could also not have a preference at all, and be ok with anything. Finally, you could just have a preference for one role, jg, and play everything else comfortably but obviously not as comfortable as fill. The solution is to include fill into the `role` enum class. Then, it could be used as a wildcard in `game_creation` with it's index still having significance, as the preference.

Additionally, after `fill`, `not ...` can be used (eg `not bot`) to signify that despite being fill, they don't want to be that role. The significance for this is to allow players to have equal preference for a select number of roles greater than 1 and less than 5. To show how it works I can enter: `--roles="jg, fill, not bot`. This would mean `jg` has number 1 priority, then `mid, top, sup` at equal preference below `jg` and finally `bot` being excluded as an option completely.

Current Issues:

- Rank/Elo could be different based on role

### Game Creation

Create game assigning 10 players filtered via player name. Will permutate all possibilities and only consider those with each player getting a role they prefer. The score is the elo difference between the team, but also considers the preference of that role. For example two comps created with the same elo difference with one having every player on their primary role, whereas the other with players on their secondary role would have a difference for the creation; in this case the first one is chosen. The created game will record the teams onto `game_data.json` for post game adjustment.

Use `--names` and make sure to seperate everything via `, `.

Current Issues:

- Should bot lane be considered differently

### Post Game Adjustment

After the game, using this tool using the `--results` option and 6 parameters (winnning team and gold difference at 15 minutes (team 1 - team 2)). These stats will reference the players in `game_data.json` and adjust the players' elo accordingly.

## Elo System

Refering to this URL: https://mattmazzola.medium.com/understanding-the-elo-rating-system-264572c7a2b4, the elo system will work on 2 layers: lane performance, and outcome of the game.

Rather then just considering the probability against your lane opponent, you will consider each player you are against. However, the lane you are against has highest value. For example, consider these teams:
| Team 1 | Team 2 |
|---------------|---------------|
| Player A: 400 | Player B: 600 |
| Player C: 500 | Player D: 500 |
| Player E: 700 | Player F: 600 |
| Player G: 500 | Player H: 700 |
| Player I: 600 | Player J: 400 |

Suppose in this case Team 2 wins. However, by some measurement, it is determined that Player A won lane. In this case the formula for Player A's new elo is as shown:

$$ R'_A = R_A + K_L(S_L-E_{AB}) + K*G(S_G-E*{AD})+K*G(S_G-E*{AF})+K*G(S_G-E*{AH})+K*G(S_G-E*{AJ})$$

Note that while $K_L$ and $K_G$ will both be based on number of games played, $K_L$ will be much larger.

Current Issues:

- The K values are not perfect and need further calibration
- Bot lane is considered seperately for bot and support, they might need to be considered as both seperate and as a lane, solely as a lane, or as it is now

## Post Game

### Winning lane

Who wins lane will be decided by the gold difference at 15 minutes. A linear equation between -1000 and 1000 determines a state between 0 (lose) and 1 (win).

### Updating

The tool will take the the information and update the elo. After which, the player is updated with the new elo and games played increasing by 1. The new elo is applied after the calculations as to not effect it.
