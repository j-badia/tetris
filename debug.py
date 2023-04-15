import pygame
from settings import *

class Debug:
    def __init__(self, screen, pos):
        self.font = pygame.font.SysFont(None, 24)
        self.screen = screen
        self.pos = pos
        self.img = None
    
    def blit(self):
        if self.img:
            self.screen.blit(self.img, self.pos)

    def clear(self):
        self.img = None

    def print(self, text):
        self.img = self.font.render(text, True, (200, 200, 200), (0, 0, 0))