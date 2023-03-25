from blockshape import BlockShape
from gamestatus import GameStatus
from tetromino import Tetromino
from legality import Legality
from copy import deepcopy


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
        self.reset_view()
    
    def reset_view(self):
        self.render_matrix = [['   ' for _ in range(self.width)] for _ in range(self.height)]
    
    def update_view(self):
        self.reset_view()
        for row in self.block_matrix:
            # print(row)
            for block in row:
                if block:
                    x,y = block.coords()
                    self.render_matrix[y][x] = ' O '
    
    def remove_active(self):
        for block in self.active_shape.blocks():
            x,y = block.coords()
            self.block_matrix[y][x] = None
    
    def add_active(self):
        for block in self.active_shape.blocks():
            x,y = block.coords()
            self.block_matrix[y][x] = block
    
    # relies on the active shape having been temporarily removed from block_matrix
    def still_falling(self):
        for block in self.active_shape.blocks():
            x,y = block.coords()
            if y < self.height-1:
                if self.block_matrix[y+1][x]:
                    return False
            else:
                return False
        return True
    
    def is_valid(self, simulated_shape: BlockShape) -> Legality:
        status = Legality.Legal
        self.remove_active()
        still_falling = self.still_falling()
        for block in simulated_shape.blocks():
            x,y = block.coords()
            if x >= self.width or x < 0:
                status = Legality.Impossible
            elif y >= self.height:
                status = Legality.Illegal
                break
            else:
                if self.block_matrix[y][x]:
                    if still_falling:
                        status = Legality.Impossible
                    else:
                        status = Legality.Illegal
                        break
        self.add_active()
        return status
    
    def _with_legality_check(self, BLOCKSHAPE_METHOD) -> GameStatus:
        simulated_shape = deepcopy(self.active_shape)
        BLOCKSHAPE_METHOD(simulated_shape)
        match self.is_valid(simulated_shape):
            case Legality.Legal:
                self.remove_active()
                BLOCKSHAPE_METHOD(self.active_shape)
                self.add_active()
            case Legality.Illegal:
                return GameStatus.EndOfTurn
            case Legality.Impossible:
                pass
        return GameStatus.Continue
    
    def get_full_rows(self) -> list[int]:
        full_rows = []
        for i,row in enumerate(self.block_matrix):
            if None not in row:
                full_rows.append(i)
        return full_rows

    def reset_block_positions(self):
        for y,row in enumerate(self.block_matrix):
            for x,block in enumerate(row):
                if block:
                    block.set_pos(x,y)

    def tick(self) -> GameStatus:
        # eventually will shift active_shape down automatically
        self.remove_active()
        full_rows = self.get_full_rows()
        if full_rows:
            for i in reversed(full_rows):
                self.block_matrix[i] = []
                for row in self.block_matrix[0:i]:
                    for block in list(filter(None, row)):
                        block.shift(d_y=1)
            new_block_matrix = list(filter(None, self.block_matrix))
            while len(new_block_matrix) < self.height:
                new_row = [None for _ in range(self.width)]
                new_block_matrix.insert(0, new_row)
            self.block_matrix = new_block_matrix
        self.add_active()
    
    def rotate_right(self) -> GameStatus:
        return self._with_legality_check(BlockShape.rotate_right)

    def rotate_left(self) -> GameStatus:
        return self._with_legality_check(BlockShape.rotate_left)

    def shift_right(self) -> GameStatus:
        return self._with_legality_check(BlockShape.shift_right)

    def shift_left(self) -> GameStatus:
        return self._with_legality_check(BlockShape.shift_left)

    def shift_down(self) -> GameStatus:
        return self._with_legality_check(BlockShape.shift_down)
    
    def hard_drop(self) -> GameStatus:
        while self.shift_down() != GameStatus.EndOfTurn:
            continue
        return GameStatus.EndOfTurn
    
    def spawn(self, shape: Tetromino):
        block_shape = BlockShape(shape)
        x,y = shape.value['spawn_offset']
        for block in block_shape.blocks():
            block.set_pos(x,y)
        self.active_shape = block_shape
        self.add_active()
