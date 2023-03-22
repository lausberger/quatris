from block import Block
from tetromino import Tetromino

class BlockShape():
    def __init__(self, shape: Tetromino):
        self.shape = shape
        self.rot_idx = 0
        self.blocks = []
        self.generate_blocks()
    
    def __str__(self):
        dims = self.shape.value[2]
        grid = [['.' for _ in range(dims[1])] for _ in range(dims[0])]
        for b in self.blocks:
            x,y = b.coords()
            grid[y][x] = 'O'
        return '\n'.join([str(row) for row in grid])
    
    def generate_blocks(self):
        rotation = self.shape.value[0][self.rot_idx]
        color = self.shape.value[1]
        self.blocks = [Block(x,y,color) for (x,y) in rotation]
    
    def delete_all(self):
        for b in self.blocks:
            b.delete()
    
    def move_down(self):
        for b in self.blocks:
            b.shift(d_y=-1)
    
    def move_right(self):
        for b in self.blocks:
            b.shift(d_x=1)
    
    def move_left(self):
        for b in self.blocks:
            b.shift(d_x=-1)
    
    def rotate_right(self):
        self.rot_idx = (self.rot_idx + 1) % 4
        self.generate_blocks()
    
    def rotate_left(self):
        self.rot_idx = (self.rot_idx - 1) % 4
        self.generate_blocks()


