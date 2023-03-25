from enum import Enum

class GameStatus(Enum):
    GameOver = -1
    EndOfTurn = 0
    Continue = 1