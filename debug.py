import pygame
from settings import *

class Debug(pygame.sprite.Sprite):
    def __init__(self, screen, pos):
        super().__init__()
        self.font = pygame.font.SysFont(None, 24)
        self.screen = screen
        self.rect = pygame.Rect(pos, (0, 0))
        self.image = pygame.Surface((0, 0))
    
    def blit(self):
        if self.image:
            self.screen.blit(self.image, self.rect)

    def clear(self):
        self.image = None

    def print(self, text):
        self.image = self.font.render(str(text), True, (200, 200, 200), (0, 0, 0))