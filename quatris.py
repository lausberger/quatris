from tetromino import Tetromino
from blockshape import BlockShape

class Game():
    def __init__(self):
        self.board = [[0] * 10] * 20

def main():
    tetrominos = list([Tetromino.__members__][0].values())
    for shape in tetrominos:
        blockshape = BlockShape(shape)
        print(shape, '\n')
        for _ in shape.value[0]:
            print(blockshape, '\n')
            blockshape.rotate_right()
        print('=========\n') 

if __name__ == "__main__":
    main()