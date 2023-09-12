from role import Role


class Player:
    id = 0
    # takes name, roles, number of games played, and elo

    def __init__(self, name: str, roles: list, games_played: int, elo: int) -> None:
        self.id = Player.id
        Player.id += 1
        self.name = name
        self.games_played = games_played
        self.elo = elo
        self.roles: list[Role] = []
        for role in roles:
            self.roles.append(Role[role])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
