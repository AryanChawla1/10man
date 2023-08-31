from __future__ import annotations
from enum import Enum
from functools import total_ordering


# Might be useless
@total_ordering
class Rank(Enum):
    LOW_IRON = 0
    HIGH_IRON = 100
    LOW_BRONZE = 200
    HIGH_BRONZE = 300
    LOW_SILVER = 400
    HIGH_SILVER = 500
    LOW_GOLD = 600
    HIGH_GOLD = 700
    LOW_PLAT = 800
    HIGH_PLAT = 900
    LOW_EMERALD = 1000
    HIGH_EMERALD = 1100
    LOW_DIAMOND = 1200
    HIGH_DIAMOND = 1300
    MASTER = 1400
    GRANDMASTER = 1500
    CHALLENGER = 1600

    def __eq__(self, __other: Rank) -> bool:
        return self.value == __other.value

    def __gt__(self, __other: Rank) -> bool:
        return self.value > __other.value

    def __le__(self, __other: Rank) -> bool:
        return self.value <= __other.value
