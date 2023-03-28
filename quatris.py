import random
import pygame
from copy import deepcopy
from blockmatrix import BlockMatrix
from gamestatus import GameStatus
from legality import Legality
from gamerenderer import GameRenderer
from tetromino import Tetromino
from blockshape import BlockShape


class Quatris():
    def __init__(self):
        self.board = BlockMatrix()
        self.status = GameStatus.Continue
        self.tetrominos = list([Tetromino.__members__][0].values())
        self.score_map = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        self.score = 0
        self.current_level = 0
        self.lines_cleared = 0
        self.tick_rate = 60
        self.drop_counter = 0
        self.input_interval = 5 # frames between registered inputs when key is held
        self.frames_until_input = { k: 0 for k in self.get_holdable_keys() }
        self.held_shape = None
        self.can_hold = True
        self.current_shapes = []
        self.generate_shapes()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.renderer = GameRenderer(self.board)
        self.renderer.generate_display()
    
    def get_input_keys(self) -> list[int]:
        return [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_j, pygame.K_k, pygame.K_h, pygame.K_ESCAPE]
    
    def get_holdable_keys(self) -> list[int]:
        return [pygame.K_a, pygame.K_s, pygame.K_d]

    def generate_shapes(self):
        if len(self.current_shapes) < 2:
            if not self.current_shapes:
                current_shape = random.choice(self.tetrominos)
            else:
                current_shape = self.current_shapes[0]
            next_shape = random.choice(self.tetrominos)
            while current_shape == next_shape:
                next_shape = random.choice(self.tetrominos)
            self.current_shapes = [current_shape, next_shape]

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
 
    def spawn_next_shape(self):
        self.board.spawn(self.current_shapes[0])
        self.status = GameStatus.Continue

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
    
    def action_with_legality_check(self, BLOCKSHAPE_ACTION_METHOD) -> GameStatus:
        simulated_shape = deepcopy(self.board.active_shape)
        BLOCKSHAPE_ACTION_METHOD(simulated_shape)
        match self.validate_move(simulated_shape):
            case Legality.Illegal:
                return GameStatus.EndOfTurn
            case Legality.Legal:
                BLOCKSHAPE_ACTION_METHOD(self.board.active_shape)
            case Legality.Impossible:
                pass
        return GameStatus.Continue

    def rotate_right(self):
        self.status = self.action_with_legality_check(BlockShape.rotate_right)

    def rotate_left(self):
        self.status = self.action_with_legality_check(BlockShape.rotate_left)

    def shift_right(self):
        self.status = self.action_with_legality_check(BlockShape.shift_right)

    def shift_left(self):
        self.status = self.action_with_legality_check(BlockShape.shift_left)

    def shift_down(self):
        self.status = self.action_with_legality_check(BlockShape.shift_down)
    
    def hard_drop(self):
        while self.status != GameStatus.EndOfTurn:
            self.shift_down()
    
    def hold_shape(self):
        if self.can_hold:
            if self.held_shape:
                prev_active = self.current_shapes.pop(0)
                self.current_shapes.insert(0, self.held_shape)
                self.held_shape = prev_active
            else:
                self.held_shape = self.current_shapes.pop(0)
            self.board.active_shape = None
            self.status = GameStatus.EndOfTurn
            self.can_hold = False
    
    def tick(self):
        self.clock.tick(self.tick_rate)
        # for holds and hard drops
        if self.status == GameStatus.EndOfTurn:
            if self.board.active_shape:
                self.can_hold = True
                self.board.add_active_to_matrix()
                self.board.active_shape = None
                self.current_shapes.pop(0)
            self.generate_shapes()
        # spawn active shape if needed
        if not self.board.active_shape:
            self.spawn_next_shape()
        # check for game over
        for block in self.board.active_shape.blocks():
            x,y = block.coords()
            if self.board.block_matrix[y][x]:
                self.status = GameStatus.GameOver
        # progress game
        if self.status == GameStatus.Continue:
            if self.drop_counter == self.get_drop_rate():
                self.shift_down()
                self.drop_counter = 0
            else:
                self.drop_counter += 1
            # update game data
            cleared_lines = self.check_board()
            self.lines_cleared += cleared_lines
            self.score += self.score_map[cleared_lines]
            self.current_level = self.lines_cleared // 10
            # re-render
            self.renderer.update_info(
                self.score, 
                self.lines_cleared, 
                self.current_level, 
                self.current_shapes, 
                self.held_shape
            )
            self.renderer.render()
    
    def start(self):
        while True:
            self.tick()
            if self.status == GameStatus.GameOver:
                while pygame.event.poll().type != pygame.QUIT:
                    pass
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tear_down()
                    break
                # reset the delay timer for holdable keys on keydown
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_a:
                            self.frames_until_input[pygame.K_a] = 0
                        case pygame.K_s:
                            self.frames_until_input[pygame.K_s] = 0
                        case pygame.K_d:
                            self.frames_until_input[pygame.K_d] = 0
                        case pygame.K_w:
                            self.hard_drop()
                        case pygame.K_j:
                            self.rotate_left()
                        case pygame.K_k:
                            self.rotate_right()
                        case pygame.K_h:
                            self.hold_shape()
                        case pygame.K_ESCAPE:
                            pass
                        case _:
                            pass
            if self.status != GameStatus.EndOfTurn:
                pressed_keys = pygame.key.get_pressed()
                for key in self.get_holdable_keys():
                    if pressed_keys[key]:
                        if self.frames_until_input[key] == 0:
                            self.frames_until_input[key] = self.input_interval
                            match key:
                                case pygame.K_a:
                                    self.shift_left()
                                case pygame.K_s:
                                    self.shift_down()
                                case pygame.K_d:
                                    self.shift_right()
                        elif self.frames_until_input[key] > 0:
                            self.frames_until_input[key] -= 1


def main():
    game = Quatris()
    game.start()


if __name__ == "__main__":
    main()
