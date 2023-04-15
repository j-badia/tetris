import pygame
from pygame.math import Vector2
from settings import *

SH_O, SH_I, SH_T, SH_J, SH_L, SH_S, SH_Z = range(7)
COLORS = [pygame.Color("yellow2"),
          pygame.Color("cyan2"),
          pygame.Color("purple3"),
          pygame.Color("orange2"),
          pygame.Color("darkblue"),
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
CENTERS = [(1, 1), (2, 1), (0.5, 0.5), (-0.5, 1.5), (1.5, 1.5), (0.5, 1.5), (1.5, 1.5)]

def screen_from_matrix(pos):
    x, y = pos
    xc, yc = MATRIX_CORNER_POS
    return (xc + BLOCK_SIZE*x, yc + BLOCK_SIZE*y)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, *groups):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        if not hasattr(type(self), "pattern"):
            Block.pattern = pygame.image.load("block.png").convert()
        self.image.blit(Block.pattern, (0, 0))
    
    def place(self, mat_pos):
        self.rect = pygame.Rect(screen_from_matrix(mat_pos), (BLOCK_SIZE, BLOCK_SIZE))


class Tetrimino(pygame.sprite.Group):
    def __init__(self, shape):
        self.shape = shape
        self.blocks = [Block(COLORS[shape]) for i in range(4)]
        super().__init__(*self.blocks)
    
    def place(self):
        for block, pos in zip(self.blocks, SHAPES[self.shape]):
            block.place(pos)
        cent_rel = Vector2(CENTERS[self.shape])
        self.rotation_center = Vector2(self.blocks[0].rect.topleft) + BLOCK_SIZE*cent_rel
    
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
    
    def update(self, fallen):
        for block in self.blocks:
            block.update()
        collided = self.test_collision(fallen)
        if collided:
            for block in self.blocks:
                block.rect.move_ip(0, -BLOCK_SIZE)
        return collided
    
    def move(self, dir, fallen):
        for block in self.blocks:
            block.rect.move_ip(dir[0]*BLOCK_SIZE, dir[1]*BLOCK_SIZE)
        collided = self.test_collision(fallen)
        if collided:
            for block in self.blocks:
                block.rect.move_ip(-dir[0]*BLOCK_SIZE, -dir[1]*BLOCK_SIZE)
        else:
            self.rotation_center += BLOCK_SIZE*Vector2(dir)
        return collided
    
    def rotate(self, key):
        for block in self.blocks:
            block_cent = Vector2(block.rect.center)
            pos_rel = block_cent - self.rotation_center
            if key == CW_KEY:
                pos_rel.rotate_ip(90)
            elif key == CCW_KEY:
                pos_rel.rotate_ip(-90)
            block.rect.center = (self.rotation_center + pos_rel)[:]