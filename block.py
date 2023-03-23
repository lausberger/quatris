from enum import Enum
from color import Color


class Block():
    # these coordinates are local to a given tetromino's block matrix
    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.x_offset = None
        self.y_offset = None
        self.color = color
        self.exists = False
    
    def coords(self) -> tuple[int, int]:
        return (self.x + self.x_offset, self.y + self.y_offset) if self.exists else None

    def local_coords(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def delete(self):
        self.x_go = None
        self.x_go = None
        self.exists = False
    
    def shift(self, d_x: int = 0, d_y: int = 0):
        self.x_offset += d_x
        self.y_offset += d_y
    
    def set_pos(self, x_offset: int, y_offset: int):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.exists = True
    
    def set_local_pos(self, x: int, y: int):
        self.x = x
        self.y = y
