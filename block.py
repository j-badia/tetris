import pygame
from pygame.math import Vector2
from settings import *

SH_O, SH_I, SH_T, SH_J, SH_L, SH_S, SH_Z = range(7)
COLORS = [pygame.Color("yellow2"),
          pygame.Color("cyan2"),
          pygame.Color("purple3"),
          pygame.Color("orange2"),
          pygame.Color("blue"),
          pygame.Color("green3"),
          pygame.Color("red2")]
SHAPES = [[(4, -2), (5, -2), (4, -1), (5, -1)],
          [(3, -1), (4, -1), (5, -1), (6, -1)],
          [(4, -2), (3, -1), (4, -1), (5, -1)],
          [(5, -2), (3, -1), (4, -1), (5, -1)],
          [(3, -2), (3, -1), (4, -1), (5, -1)],
          [(4, -2), (5, -2), (3, -1), (4, -1)],
          [(3, -2), (4, -2), (4, -1), (5, -1)]]
# The centers are the centers of rotation, relative to the top-left corner of the first block in the shape's list
CENTERS = list(map(Vector2, [(1, 1), (2, 1), (0.5, 0.5), (-0.5, 1.5), (1.5, 1.5), (0.5, 1.5), (1.5, 1.5)]))
ROT_MOVEMENTS = list(map(Vector2, [(1,0), (-1,0), (0,1), (1,1), (-1,1)]))
ROT_MOVEMENTS_I = list(map(Vector2, [(1,0), (2,0), (-1,0), (-2,0), (0,1), (1,1), (-1,1)]))

def screen_from_matrix(pos):
    x, y = pos
    xc, yc = MATRIX_CORNER_POS
    return (xc + BLOCK_SIZE*x, yc + BLOCK_SIZE*y)

def matrix_from_screen(pos):
    x, y = pos
    xc, yc = MATRIX_CORNER_POS
    xm = (x - xc)/BLOCK_SIZE
    ym = (y - yc)/BLOCK_SIZE
    return (xm, ym)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, *groups):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color, (1, 1, BLOCK_SIZE-2, BLOCK_SIZE-2))
    
    def place(self, mat_pos):
        self.rect = pygame.Rect(screen_from_matrix(mat_pos), (BLOCK_SIZE, BLOCK_SIZE))
        self.mat_pos = Vector2(mat_pos)

    def move(self, dir):
        self.rect.move_ip((BLOCK_SIZE*dir)[:])
        self.mat_pos += dir
    
    def move_to(self, mat_pos):
        self.mat_pos = mat_pos
        self.rect.topleft = screen_from_matrix(mat_pos)

class Tetrimino(pygame.sprite.Group):
    def __init__(self, shape):
        self.shape = shape
        self.blocks = [Block(COLORS[shape]) for i in range(4)]
        super().__init__(*self.blocks)
    
    def place(self, center=None):
        for block, pos in zip(self.blocks, SHAPES[self.shape]):
            block.place(Vector2(pos))
        cent_rel = CENTERS[self.shape]
        self.rotation_center = self.blocks[0].mat_pos + cent_rel
        if center is not None:
            self.move_no_collision(Vector2(center) - self.rotation_center)
    
    def test_collision(self, others):
        for block in self.blocks:
            if pygame.sprite.spritecollideany(block, others):
                return True
            if block.rect.bottom > MATRIX_CORNER_POS[1] + BLOCK_SIZE*MATRIX_SIZE[1]:
                return True
            if block.rect.left < MATRIX_CORNER_POS[0]:
                return True
            if block.rect.right > MATRIX_CORNER_POS[0] + BLOCK_SIZE*MATRIX_SIZE[0]:
                return True
        return False
    
    def move_no_collision(self, dir):
        for block in self.blocks:
            block.move(dir)
        self.rotation_center += Vector2(dir)

    def move(self, dir, fallen):
        dir_v = Vector2(dir)
        self.move_no_collision(dir_v)
        collided = self.test_collision(fallen)
        if collided:
            self.move_no_collision(-dir_v)
        return collided
    
    def rotated_no_collision(self, key):
        positions = []
        for block in self.blocks:
            block_cent = block.mat_pos + Vector2(0.5, 0.5)
            pos_rel = block_cent - self.rotation_center
            if key in CW_KEYS:
                pos_rel.rotate_ip(90)
            elif key in CCW_KEYS:
                pos_rel.rotate_ip(-90)
            positions.append((self.rotation_center + pos_rel - Vector2(0.5, 0.5))[:])
        return positions
    
    def rotate(self, key, fallen):
        old_positions = [block.mat_pos for block in self.blocks]
        positions = self.rotated_no_collision(key)
        for block, pos in zip(self.blocks, positions):
            block.move_to(pos)
        if self.test_collision(fallen):
            deltas = ROT_MOVEMENTS_I if self.shape==SH_I else ROT_MOVEMENTS
            for delta in deltas:
                collided = self.move(delta, fallen)
                if not collided:
                    return
            for block, pos in zip(self.blocks, old_positions):
                block.move_to(pos)

class Fallen(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.matrix = {}
        for i in range(MATRIX_SIZE[0]):
            for j in range(MATRIX_SIZE[1]):
                self.matrix[(i, j)] = None
        self.completed_lines = []
    
    def add_block(self, block, pos=None):
        if pos is None:
            pos = block.mat_pos
        self.matrix[tuple(pos[:])] = block
        super().add(block)
    
    def get(self, i, j=None):
        if j is None:
            i, j = i
        return self.matrix[(i, j)]
    
    def get_row(self, j):
        return [self.matrix[(i, j)] for i in range(MATRIX_SIZE[0])]
    
    def set_row(self, j, blocks):
        for i, block in enumerate(blocks):
            if block is not None:
                block.move_to(Vector2(i, j))
            self.matrix[(i, j)] = block
    
    def clear_line(self, j):
        self.remove(self.get_row(j))
        self.set_row(j, MATRIX_SIZE[0]*[None])

    def move_completed_lines(self):
        for j in sorted(self.completed_lines):
            for jp in reversed(range(j)):
                self.set_row(jp+1, self.get_row(jp))
            self.set_row(0, MATRIX_SIZE[0]*[None])
        self.completed_lines = []

    def clear_lines(self):
        for j in self.completed_lines:
            self.clear_line(j)        
    
    def check_lines(self):
        if len(self.completed_lines) > 0:
            return self.completed_lines
        self.completed_lines = []
        for j in reversed(range(MATRIX_SIZE[1])):
            complete_line = True
            for elem in self.get_row(j):
                if elem is None:
                    complete_line = False
            if complete_line:
                self.completed_lines.append(j)
        return self.completed_lines
    
    def paint_line(self, j):
        for i in range(MATRIX_SIZE[0]):
            self.get(i, j).image.fill((230, 230, 230))

    def paint_lines(self):
        for j in self.completed_lines:
            self.paint_line(j)