import pygame
from pygame.locals import *
from settings import *
from block import Block

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    background = pygame.image.load("background.png")
    background = background.convert()

    queue = pygame.sprite.Group()
    tetrimino = pygame.sprite.Group()
    fallen = pygame.sprite.Group()
    groups = [queue, tetrimino, fallen]
    groups_draw = [tetrimino, fallen]

    test_blocks = [Block(color, tetrimino) for color in [(255, 100, 100), (100, 255, 100), (100, 100, 255)]]
    for i, block in enumerate(test_blocks):
        block.place((i, 2))
    #screen.blit(test_block.image, test_block.rect)

    screen_update = pygame.event.custom_type()
    block_fall = pygame.event.custom_type()
    pygame.time.set_timer(screen_update, int(1000/60))
    pygame.time.set_timer(block_fall, 750)

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == screen_update:
                for group in groups_draw:
                    group.draw(screen)
                pygame.display.flip()
            if event.type == block_fall:
                tetrimino.update()   

if __name__ == "__main__":
    main()