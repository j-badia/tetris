import pygame
from settings import *

def screen_from_matrix(pos):
    x, y = pos
    xc, yc = MATRIX_CORNER_POS
    return (xc + BLOCK_SIZE*x, yc + BLOCK_SIZE*y)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("block.png")
        self.image = self.image.convert()
        self.image.fill(color, (2, 2, BLOCK_SIZE-2, BLOCK_SIZE-2))
    
    def place(self, mat_pos):
        self.rect = pygame.Rect(screen_from_matrix(mat_pos), (BLOCK_SIZE, BLOCK_SIZE))
    
    def update(self):
        self.rect.move_ip(0, BLOCK_SIZE)