from color import Color


class Block():
    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.x_offset = None
        self.y_offset = None
        self.color = color
    
    def coords(self) -> tuple[int, int]:
        return (self.x + self.x_offset, self.y + self.y_offset)

    def local_coords(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def shift(self, d_x: int = 0, d_y: int = 0):
        self.x_offset += d_x
        self.y_offset += d_y
    
    def set_pos(self, x_offset: int, y_offset: int):
        self.x_offset = x_offset
        self.y_offset = y_offset
    
    def set_local_pos(self, x: int, y: int):
        self.x = x
        self.y = y
