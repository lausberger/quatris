from enum import Enum
from color import Color


class Block():
    # these coordinates are local to a given tetromino's block matrix
    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.global_x = None
        self.global_y = None
        self.color = color
    
    def coords(self):
        return (self.x, self.y)
    
    def global_coords(self):
        return (self.global_x, self.global_y)
    
    def delete(self):
        self.global_x = None
        self.global_y = None
    
    def shift(self, d_x: int = 0, d_y: int = 0):
        self.global_x += d_x
        self.global_y += d_y
    
    def setpos(self, x: int, y: int):
        self.global_x = x
        self.global_y = y
