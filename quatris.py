import random
from block import Block
from blockmatrix import BlockMatrix
from gamestatus import GameStatus
from tetromino import Tetromino
from blockshape import BlockShape
from getkey import getkey, keys

class Quatris():
    def __init__(self):
        self.board = BlockMatrix()

def main():
    tetrominos = list([Tetromino.__members__][0].values())
    board = BlockMatrix()
    while True:
        shape = random.choice(tetrominos)
        board.spawn(shape)
        board.update_view()
        print(board)
        while True:
            key = getkey()
            board.tick()
            match key.upper():
                case 'W':
                    status = board.hard_drop()
                case 'A':
                    status = board.shift_left()
                case 'D':
                    status = board.shift_right()
                case 'S':
                    status = board.shift_down()
                case 'J':
                    status = board.rotate_left()
                case 'K':
                    status = board.rotate_right()
                case _:
                    continue
            board.update_view()
            print(board)
            match status:
                case GameStatus.Continue:
                    pass
                case GameStatus.EndOfTurn:
                    board.active_shape = None
                    break
                case GameStatus.GameOver:
                    exit(0)
    

if __name__ == "__main__":
    main()