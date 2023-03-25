import pygame
from pygame.locals import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 720))
    pygame.display.set_caption("Tetris")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

if __name__ == "__main__":
    main()