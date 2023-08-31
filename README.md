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

Create players using `player_creator.py`. Make sure to include `--name`, `--rank`, and `--role`. Rank must be low/high of rank, with the exception of master, grandmater and challenger. Role should be prioritized; `fill` can be used for all roles.
Created player will start off with elo solely considering the rank, however, as games continue, a proper elo will be calculated based on performance and lane performance.

Current Issues:

- If you play all five roles, or fill, there currently isn't a way to set a preference for them, it will assume you equally prefer all of them.
- Rank/Elo could be different based on role

### Game Creation

Create game assigning 10 players filtered via player name. Will permutate all possibilities and only consider those with each player getting a role they prefer. The score is the elo difference between the team, but also considers the preference of that role. For example two comps created with the same elo difference with one having every player on their primary role, whereas the other with players on their secondary role would have a difference for the creation; in this case the first one is chosen.

Use `--names` and make sure to seperate everything via `, `.

Current Issues:

- Matchup disparities should be deincentivized, this should be added
- Currently, the punishment for having players in the second role is not that big of a decision factor in teammaking, should be discussed

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

## Post Game

### Winning lane

Who wins lane will be decided by the gold difference at 15 minutes. Within 500 gold difference is considered equal, however any more will be considered a win or lose. This is a little weird for junglers, we will see how it goes.

### Updating (IN PROGRESS)

After the game, the elo needs to be updated cleanly. Looking for suggestions! the lane stats at 15 minutes (the program can decide it or maybe the lane result can be provided), game results (win or loss), and teams (just in case they are different then what was outputted) should be provided. JSON needs to be updated
