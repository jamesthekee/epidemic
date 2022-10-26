import enum


class State(enum.Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    REMOVED = 2
    VACCINATED = 3
    EXPOSED = 4


class Policy(enum.Enum):
    NONE = 0
    PARTIAL = 1
    FREE_ = 2
