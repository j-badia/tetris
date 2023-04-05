import pygame
from settings import *

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
    
    def update(self, fallen):
        collide = False
        for block in self.blocks:
            block.update()
            if not collide:
                if pygame.sprite.spritecollideany(block, fallen) or block.rect.bottom > MATRIX_CORNER_POS[1]+BLOCK_SIZE*MATRIX_SIZE[1]:
                    collide = True
        if collide:
            for block in self.blocks:
                block.rect.move_ip(0, -BLOCK_SIZE)
        return collide
    
    def move(self, dir, fallen):
        collide = False
        for block in self.blocks:
            block.rect.move_ip(dir*BLOCK_SIZE, 0)
            if not collide:
                if pygame.sprite.spritecollideany(block, fallen) or block.rect.left < MATRIX_CORNER_POS[0] or block.rect.right > MATRIX_CORNER_POS[0]+BLOCK_SIZE*MATRIX_SIZE[0]:
                    collide = True
        if collide:
            for block in self.blocks:
                block.rect.move_ip(-dir*BLOCK_SIZE, 0)