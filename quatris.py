import random
from block import Block
from blockmatrix import BlockMatrix
from color import Color
from gamestatus import GameStatus
from legality import Legality
from tetromino import Tetromino
from blockshape import BlockShape
from copy import deepcopy
import pygame

class Quatris():
    def __init__(self):
        self.board = BlockMatrix()
        self.status = GameStatus.Continue
        self.score_map = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        self.score = 0
        self.current_level = 0
        self.lines_cleared = 0
        self.tick_rate = 60
        self.input_interval = 300 # ms between inputs
        self.input_delay = 100
        self.dt = 0
        self.generate_display()

    def generate_display(self):
        self.block_size = 20
        self.disp_height = self.block_size * self.board.height + 10
        self.disp_width = self.block_size * self.board.width + 10
        self.m_x_start = 5
        self.m_x_end = self.disp_width - 5
        self.m_y_start = 5
        self.m_y_end = self.disp_height - 5
        pygame.init()
        pygame.key.set_repeat(0, self.input_interval)
        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))
        self.screen.fill(Color.WHITE.value)
        self.clock = pygame.time.Clock()
    
    def render(self):
        for x, x_dim in enumerate(range(self.m_x_start, self.m_x_end, self.block_size)):
            for y, y_dim in enumerate(range(self.m_y_start, self.m_y_end, self.block_size)):
                square = pygame.Rect(x_dim, y_dim, self.block_size, self.block_size)
                block = self.board.block_matrix[y][x]
                if block:
                    pygame.draw.rect(self.screen, block.color.value, square, 0)
                else:
                    pygame.draw.rect(self.screen, Color.BLACK.value, square, 0)
                pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)
        # this shouldn't be required; fix game loop
        if self.board.active_shape:
            for block in self.board.active_shape.blocks():
                x,y = block.coords()
                x_dim = self.m_x_start + (x * self.block_size)
                y_dim = self.m_y_start + (y * self.block_size)
                square = pygame.Rect(x_dim, y_dim, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, block.color.value, square, 0)
                pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)

    def get_drop_rate(self):
        match self.current_level:
            case 0: return 48
            case 1: return 43
            case 2: return 38
            case 3: return 33
            case 4: return 28
            case 5: return 23
            case 6: return 18
            case 7: return 13
            case 8: return 8
            case 9: return 6
            case n if 10 <= n <= 12: return 5
            case n if 13 <= n <= 15: return 4
            case n if 16 <= n <= 18: return 3
            case n if 19 <= n <= 28: return 2
            case _: return 1
    
    def get_full_rows(self) -> list[int]:
        full_rows = []
        for i,row in enumerate(self.board.block_matrix):
            if None not in row:
                full_rows.append(i)
        return full_rows

    def check_board(self) -> int:
        full_rows = self.get_full_rows()
        cleared_lines = len(full_rows)
        if cleared_lines:
            for i in reversed(full_rows):
                self.board.block_matrix[i] = []
                for row in self.board.block_matrix[0:i]:
                    for block in list(filter(None, row)):
                        block.shift(d_y=1)
            new_block_matrix = list(filter(None, self.board.block_matrix))
            while len(new_block_matrix) < self.board.height:
                new_row = [None for _ in range(self.board.width)]
                new_block_matrix.insert(0, new_row)
            self.board.block_matrix = new_block_matrix
        return cleared_lines

    def tick(self):
        cleared_lines = self.check_board()
        self.lines_cleared += cleared_lines
        self.score += self.score_map[cleared_lines]
        self.current_level = self.lines_cleared // 10
        print('lines cleared',self.lines_cleared)
        print('level',self.current_level)
        print('score',self.score)

    def tear_down(self):
        self.board.reset()
        pygame.quit()

    def active_is_falling(self):
        for block in self.board.active_shape.blocks():
            x,y = block.coords()
            if y >= self.board.height-1:
                return False
            if self.board.block_matrix[y+1][x]:
                return False
        return True

    def validate_move(self, simulated_shape: BlockShape) -> Legality:
        status = Legality.Legal
        for block in simulated_shape.blocks():
            x,y = block.coords()
            if x >= self.board.width or x < 0:
                status = Legality.Impossible
            elif y >= self.board.height:
                status = Legality.Illegal
                break
            else:
                if self.board.block_matrix[y][x]:
                    if self.active_is_falling():
                        status = Legality.Impossible
                    else:
                        status = Legality.Illegal
                        break
        return status
    
    def _with_legality_check(self, BLOCKSHAPE_METHOD) -> GameStatus:
        simulated_shape = deepcopy(self.board.active_shape)
        BLOCKSHAPE_METHOD(simulated_shape)
        match self.validate_move(simulated_shape):
            case Legality.Illegal:
                return GameStatus.EndOfTurn
            case Legality.Legal:
                BLOCKSHAPE_METHOD(self.board.active_shape)
            case Legality.Impossible:
                pass
        return GameStatus.Continue

    def rotate_right(self) -> GameStatus:
        self.status = self._with_legality_check(BlockShape.rotate_right)

    def rotate_left(self) -> GameStatus:
        self.status = self._with_legality_check(BlockShape.rotate_left)

    def shift_right(self) -> GameStatus:
        self.status = self._with_legality_check(BlockShape.shift_right)

    def shift_left(self) -> GameStatus:
        self.status = self._with_legality_check(BlockShape.shift_left)

    def shift_down(self) -> GameStatus:
        self.status = self._with_legality_check(BlockShape.shift_down)
    
    def hard_drop(self) -> GameStatus:
        while self.status != GameStatus.EndOfTurn:
            self.shift_down()
            continue

def main():
    tetrominos = list([Tetromino.__members__][0].values())
    game = Quatris()
    game.board.spawn(random.choice(tetrominos))
    c = 0
    while True:
        game.render()
        game.status = GameStatus.Continue
        if not game.board.active_shape:
            game.board.spawn(random.choice(tetrominos))
        game.tick()
        if c == game.get_drop_rate():
            game.shift_down()
            c = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.tear_down()
                break
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        game.hard_drop()
                    case pygame.K_a:
                        game.shift_left()
                    case pygame.K_s:
                        game.shift_down()
                    case pygame.K_d:
                        game.shift_right()
                    case pygame.K_j:
                        game.rotate_left()
                    case pygame.K_k:
                        game.rotate_right()
                    case pygame.K_h:
                        pass
                    case pygame.K_ESCAPE:
                        pass
                    case _:
                        pass
        match game.status:
            case GameStatus.Continue:
                pass
            case GameStatus.EndOfTurn:
                game.board.add_active_to_matrix()
                game.board.active_shape = None
            case GameStatus.GameOver:
                game.tear_down()
                exit(0)
        pygame.display.update()
        game.dt = game.clock.tick(game.tick_rate)
        c += 1
    

if __name__ == "__main__":
    main()