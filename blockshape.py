from block import Block
from tetromino import Tetromino


class BlockShape():
    def __init__(self, shape: Tetromino):
        self.shape = shape
        self.rot_idx = 0
        self.block_set = {0: None, 1: None, 2: None, 3: None}
        self.initialize_blocks()
    
    def blocks(self) -> list[Block]:
        return self.block_set.values()

    def initialize_blocks(self):
        position = self.shape.value['rotations'][0]
        color = self.shape.value['color']
        for i in range(4):
            x,y = position[i]
            self.block_set[i] = Block(x,y,color)
    
    def update_rotation(self):
        position = self.shape.value['rotations'][self.rot_idx]
        for i, block in enumerate(self.blocks()):
            x,y = position[i]
            block.set_local_pos(x,y)

    def rotate_right(self):
        self.rot_idx = (self.rot_idx + 1) % 4
        self.update_rotation()
    
    def rotate_left(self):
        self.rot_idx = (self.rot_idx - 1) % 4
        self.update_rotation()
    
    def shift_right(self):
        for b in self.blocks():
            b.shift(d_x=1)
    
    def shift_left(self):
        for b in self.blocks():
            b.shift(d_x=-1)
    
    def shift_down(self):
        for b in self.blocks():
            b.shift(d_y=1)
