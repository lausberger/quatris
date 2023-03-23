from block import Block
from blockmatrix import BlockMatrix
from tetromino import Tetromino
from blockshape import BlockShape
from getkey import getkey, keys

class Quatris():
    def __init__(self):
        self.board = [[0] * 10] * 20

def main():
    tetrominos = list([Tetromino.__members__][0].values())
    # for shape in tetrominos:
    #     blockshape = BlockShape(shape)
    #     print(shape, '\n')
    #     for _ in shape.value[0]:
    #         print(blockshape, '\n')
    #         blockshape.rotate_right()
    #     print('=========\n')

    for shape in tetrominos:
        board = BlockMatrix()
        board.spawn(shape)
        board.update_view()
        print(board)
        try:
            while True:
                key = getkey()
                board.tick()
                match key.upper():
                    case 'W':
                        #board.shift_down()
                        board.hard_drop()
                    case 'A':
                        board.shift_left()
                    case 'D':
                        board.shift_right()
                    case 'S':
                        board.shift_down()
                    case 'J':
                        board.rotate_left()
                    case 'K':
                        board.rotate_right()
                    case _:
                        continue
                board.update_view()
                print(board)
        except KeyboardInterrupt:
            raise
        except:
            print('\n' + ' ' * (board.width-1) + 'G A M E  O V E R\n')
    

if __name__ == "__main__":
    main()