import math
from blockshape import BlockShape
from tetromino import Tetromino


class BlockMatrix():
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.block_matrix = []
        self.render_matrix = [['   ' for _ in range(width)] for _ in range(height)]
        self.active_shape = None
        # self.shapes = []
    
    # def __str__(self):
    #     return '\n'.join(str(row) for row in self.render_matrix)
    
    def __str__(self):
        string = ''
        for row in self.render_matrix:
            string += '||' + ''.join(row) + '||\n'
        # string = ('||' + '   ' * (self.width) + '||\n') * self.height
        string += '||' + '___' * (self.width) + '||\n\n'
        string += ' ' * (self.width * 2 - 7) + 'QUATRIS'
        return string
    
    def reset(self):
        # self.shapes = []
        self.active_shape = None
        self.block_matrix = []
        self.reset_view()
    
    def reset_view(self):
        self.render_matrix = [['   ' for _ in range(self.width)] for _ in range(self.height)]
    
    def update_view(self):
        self.reset_view()
        for block in self.block_matrix:
            if block.exists:
                x,y = block.coords()
                self.render_matrix[y][x] = ' O '
    
    def tick(self):
        # check for lines to remove
        self.active_shape.shift_down()
    
    def rotate_right(self):
        self.active_shape.rotate_right()

    def rotate_left(self):
        self.active_shape.rotate_left()
    
    def shift_right(self):
        self.active_shape.shift_right()

    def shift_left(self):
        self.active_shape.shift_left()

    def shift_down(self):
        self.active_shape.shift_down()
    
    def hard_drop(self):
        return # checks and such
    
    def spawn(self, shape: Tetromino):
        block_shape = BlockShape(shape)
        x,y = shape.value['spawn_offset']
        for i in range(4):
            block = block_shape.blocks[i]
            block.set_pos(x,y)
            self.block_matrix.append(block)
        self.active_shape = block_shape
        # self.update_view()
