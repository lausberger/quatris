from blockshape import BlockShape
from tetromino import Tetromino


class BlockMatrix():
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.block_list = []
        self.block_matrix = [[None for _ in range(width)] for _ in range(height)]
        self.render_matrix = [['   ' for _ in range(width)] for _ in range(height)]
        self.active_shape = None
    
    def __str__(self):
        string = ''
        for row in self.render_matrix:
            string += '||' + ''.join(row) + '||\n'
        string += '||' + '___' * (self.width) + '||\n\n'
        string += ' ' * (self.width * 2 - 7) + 'QUATRIS'
        return string
    
    def reset(self):
        self.active_shape = None
        self.block_list = []
        self.block_matrix = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def add_active_to_matrix(self):
        for block in self.active_shape.blocks():
            x,y = block.coords()
            self.block_matrix[y][x] = block
    
    def spawn(self, shape: Tetromino):
        self.active_shape = BlockShape(shape)
        x,y = shape.value['spawn_offset']
        for block in self.active_shape.blocks():
            block.set_pos(x,y)
