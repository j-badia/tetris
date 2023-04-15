import pygame
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
    
    def update(self):
        self.rect.move_ip(0, BLOCK_SIZE)

class Tetrimino(pygame.sprite.Group):
    def __init__(self, shape):
        self.shape = shape
        self.blocks = [Block(COLORS[shape]) for i in range(4)]
        super().__init__(*self.blocks)
    
    def place(self):
        for block, pos in zip(self.blocks, SHAPES[self.shape]):
            block.place(pos)
    
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
        return collided