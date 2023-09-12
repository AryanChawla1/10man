# from __future__ import annotations
# from functools import total_ordering
from enum import Enum


# So indices can be aligned with role
class Role(Enum):
    FILL = -1
    TOP = 0
    JG = 1
    MID = 2
    BOT = 3
    SUP = 4
    NOT_TOP = 5
    NOT_JG = 6
    NOT_MID = 7
    NOT_BOT = 8
    NOT_SUP = 9
