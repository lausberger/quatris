import pygame
from blockmatrix import BlockMatrix
from color import Color
from tetromino import Tetromino


class GameRenderer():
    def __init__(self, board: BlockMatrix):
        self.board = board
        # fonts
        self.nes_font = pygame.font.Font('fonts/Pixel_NES.ttf', 18)
        self.logo_font = pygame.font.Font('fonts/friz-quadrata-bold-cyrillic.ttf', 30)
        self.footer_font = pygame.font.Font('fonts/Pixel_NES.ttf', 12)
        # constants
        self.block_size = 20
        self.p_block_size = int(self.block_size * .75)
        self.border_width = 5
        # hold block preview
        self.h_x_start = self.border_width
        self.h_x_end = self.h_x_start + self.p_block_size * 4
        self.h_y_start = self.border_width + self.nes_font.get_height()
        self.h_y_end = self.h_y_start + self.p_block_size * 4
        # block matrix
        self.m_x_start = self.h_x_end + self.border_width
        self.m_x_end = self.m_x_start + self.block_size * self.board.width
        self.m_y_start = self.border_width
        self.m_y_end = self.border_width + self.block_size * self.board.height
        # next block preview
        self.p_x_start = self.m_x_end + self.border_width
        self.p_x_end = self.p_x_start + self.p_block_size * 4
        self.p_y_start = self.border_width + self.nes_font.get_height()
        self.p_y_end = self.p_y_start + self.p_block_size * 4
        # info box
        self.info_x_start = self.p_x_start
        self.info_x_end = self.info_x_start + self.p_block_size * 8
        self.info_y_start = self.p_y_end + self.border_width
        self.info_y_end = self.info_y_start + self.p_block_size * 6
        # game window
        self.disp_width = self.info_x_end + self.border_width
        self.disp_height = self.m_y_end + self.border_width + self.logo_font.get_height() + self.footer_font.get_height()

    def update_info(self, score: int, lines_cleared: int, current_level: int, current_shapes: list[Tetromino], held_shape: Tetromino):
        self.score = score
        self.lines_cleared = lines_cleared
        self.current_level = current_level
        self.current_shapes = current_shapes
        self.held_shape = held_shape

    def generate_display(self):
        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))
        pygame.display.set_caption('Quatris')
        pygame.display.set_icon(pygame.image.load('icons/icon.png'))
        self.screen.fill(Color.GRAY.value)

    def draw_block_matrix(self):
        # block matrix
        for x, x_dim in enumerate(range(self.m_x_start, self.m_x_end, self.block_size)):
            for y, y_dim in enumerate(range(self.m_y_start, self.m_y_end, self.block_size)):
                square = pygame.Rect(
                    x_dim, 
                    y_dim, 
                    self.block_size, 
                    self.block_size
                )
                block = self.board.block_matrix[y][x]
                if block:
                    pygame.draw.rect(self.screen, block.color.value, square, 0)
                else:
                    pygame.draw.rect(self.screen, Color.BLACK.value, square, 0)
                pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)
        # active shape
        for block in self.board.active_shape.blocks():
            x,y = block.coords()
            x_dim = self.m_x_start + (x * self.block_size)
            y_dim = self.m_y_start + (y * self.block_size)
            square = pygame.Rect(
                x_dim, 
                y_dim, 
                self.block_size, 
                self.block_size
            )
            pygame.draw.rect(self.screen, block.color.value, square, 0)
            pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)

    def draw_block_preview(self):
        # 4x4 preview window
        for x in range(4):
            for y in range(4):
                square = pygame.Rect(
                    self.p_x_start + (self.p_block_size * x), 
                    self.p_y_start + (self.p_block_size * y), 
                    self.p_block_size, 
                    self.p_block_size
                )
                pygame.draw.rect(self.screen, Color.BLACK.value, square, 0)
        # preview piece with offset if needed
        next_block = self.current_shapes[1]
        x_dim, y_dim = next_block.value['dimensions']
        x_offset = 0 if y_dim == 4 else self.p_block_size * 0.5
        y_offset = 0 if x_dim == 4 else self.p_block_size
        for x in range(x_dim):
            for y in range(y_dim):
                square = pygame.Rect(
                    x_offset + self.p_x_start + (self.p_block_size * x), 
                    y_offset + self.p_y_start + (self.p_block_size * y), 
                    self.p_block_size, 
                    self.p_block_size
                )
                if (x,y) in next_block.value['rotations'][0]:
                    pygame.draw.rect(self.screen, next_block.value['color'].value, square, 0)
                    pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)

    def draw_hold_block(self):
        # 4x4 preview window
        for x in range(4):
            for y in range(4):
                square = pygame.Rect(
                    self.h_x_start + (self.p_block_size * x), 
                    self.h_y_start + (self.p_block_size * y), 
                    self.p_block_size, 
                    self.p_block_size
                )
                pygame.draw.rect(self.screen, Color.BLACK.value, square, 0)
        # hold piece with offset if needed
        if self.held_shape:
            x_dim, y_dim = self.held_shape.value['dimensions']
            x_offset = 0 if y_dim == 4 else self.p_block_size * 0.5
            y_offset = 0 if x_dim == 4 else self.p_block_size
            for x in range(x_dim):
                for y in range(y_dim):
                    square = pygame.Rect(
                        x_offset + self.h_x_start + (self.p_block_size * x), 
                        y_offset + self.h_y_start + (self.p_block_size * y), 
                        self.p_block_size, 
                        self.p_block_size
                    )
                    if (x,y) in self.held_shape.value['rotations'][0]:
                        pygame.draw.rect(self.screen, self.held_shape.value['color'].value, square, 0)
                        pygame.draw.rect(self.screen, Color.GRAY.value, square, 1)

    def draw_game_info(self):
        # black box
        for x in range(8):
            for y in range(10):
                square = pygame.Rect(
                    self.info_x_start + (self.p_block_size * x), 
                    self.info_y_start + (self.p_block_size * y), 
                    self.p_block_size, 
                    self.p_block_size
                )
                pygame.draw.rect(self.screen, Color.BLACK.value, square, 0)
        # score
        score_text = self.nes_font.render('Score', False, Color.WHITE.value)    
        self.screen.blit(
            score_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start
            )
        )
        # score number
        score_num_text = self.nes_font.render(str(self.score), False, Color.WHITE.value)
        self.screen.blit(
            score_num_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start + self.nes_font.get_height()
            )
        )
        # lines
        lines_text = self.nes_font.render('Lines', False, Color.WHITE.value)
        self.screen.blit(
            lines_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start + self.nes_font.get_height() * 2 + self.border_width
            )
        )
        # lines number
        lines_num_text = self.nes_font.render(str(self.lines_cleared), False, Color.WHITE.value)
        self.screen.blit(
            lines_num_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start + self.nes_font.get_height() * 3 + self.border_width
            )
        )
        # level
        level_text = self.nes_font.render('Level', False, Color.WHITE.value)
        self.screen.blit(
            level_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start + self.nes_font.get_height() * 4 + self.border_width * 2
            )
        )
        # level number
        level_num_text = self.nes_font.render(str(self.current_level), False, Color.WHITE.value
        )
        self.screen.blit(
            level_num_text, 
            (
                self.info_x_start + self.border_width, 
                self.info_y_start + self.nes_font.get_height() * 5 + self.border_width * 2
            )
        )
    
    def draw_text(self):
        # hold shape
        hold_text = self.nes_font.render('Hold', False, Color.WHITE.value
        )
        self.screen.blit(
            hold_text, 
            (
                (self.h_x_end + self.h_x_start) // 2 - hold_text.get_width() // 2, 
                self.border_width
            )
        )
        # next shape
        next_text = self.nes_font.render('Next', False, Color.WHITE.value)
        self.screen.blit(
            next_text, 
            (
                (self.p_x_end + self.p_x_start) // 2 - next_text.get_width() // 2, 
                self.border_width
            )
        )
        # logo
        quatris_text = self.logo_font.render('QUATRIS', False, Color.WHITE.value)
        self.screen.blit(
            quatris_text, 
            (
                self.disp_width // 2 - quatris_text.get_width() // 2, 
                self.m_y_end
            )
        )
        # credits
        lucas_text = self.footer_font.render('Lucas Ausberger, March 2023', False, Color.WHITE.value)
        self.screen.blit(
            lucas_text,
            (
                self.disp_width // 2 - lucas_text.get_width() // 2,
                self.m_y_end + quatris_text.get_height()
            )
        )
    
    def render(self):
        self.draw_block_matrix()
        self.draw_block_preview()
        self.draw_hold_block()
        self.draw_text()
        self.draw_game_info()
        pygame.display.update()
