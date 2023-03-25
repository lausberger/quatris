from block import Block
from tetromino import Tetromino

class BlockShape():
    def __init__(self, shape: Tetromino):
        self.shape = shape
        self.rot_idx = 0
        self.block_set = {0: None, 1: None, 2: None, 3: None}
        self.initialize_blocks()
    
    def __str__(self):
        w,h = self.shape.value['print_size']
        grid = [['.' for _ in range(h)] for _ in range(w)]
        for b in self.blocks():
            x,y = b.local_coords()
            grid[y][x] = 'O'
        return '\n'.join([str(row) for row in grid])
    
    def blocks(self) -> list[Block]:
        return self.block_set.values()
    
    def has_block(self, block: Block) -> bool:
        return block in self.blocks()
    
    def initialize_blocks(self):
        position = self.shape.value['rotations'][0]
        color = self.shape.value['color']
        for i in range(4):
            x,y = position[i]
            self.block_set[i] = Block(x,y,color)
    
    def update_blocks(self):
        position = self.shape.value['rotations'][self.rot_idx]
        for i, block in enumerate(self.blocks()):
            x,y = position[i]
            block.set_local_pos(x,y)
        # for i in range(4):
        #     x,y = position[i]
        #     self.blocks[i].set_local_pos(x,y)
    
    def delete_all(self):
        self.block_set = {0: None, 1: None, 2: None, 3: None}

    def rotate_right(self):
        self.rot_idx = (self.rot_idx + 1) % 4
        self.update_blocks()
    
    def rotate_left(self):
        self.rot_idx = (self.rot_idx - 1) % 4
        self.update_blocks()
    
    def shift_right(self):
        for b in self.blocks():
            b.shift(d_x=1)
    
    def shift_left(self):
        for b in self.blocks():
            b.shift(d_x=-1)
    
    def shift_down(self):
        for b in self.blocks():
            b.shift(d_y=1)
