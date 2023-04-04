import pygame
from pygame.locals import *
from settings import *
from block import Block, Tetrimino

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    background = pygame.image.load("background.png")
    background = background.convert()

    queue = pygame.sprite.Group()
    #tetrimino = pygame.sprite.Group()
    fallen = pygame.sprite.Group()

    #test_blocks = [Block(color, tetrimino) for color in [(255, 100, 100), (100, 255, 100), (100, 100, 255)]]
    #for i, block in enumerate(test_blocks):
    #    block.place((i, 2))
    #screen.blit(test_block.image, test_block.rect)
    tetrimino = Tetrimino(SH_J)

    screen_update = pygame.event.custom_type()
    block_fall = pygame.event.custom_type()
    pygame.time.set_timer(screen_update, int(1000/60))
    pygame.time.set_timer(block_fall, 500)

    auto_repeat_left = pygame.event.custom_type()
    auto_repeat_right = pygame.event.custom_type()
    move_left = pygame.event.custom_type()
    move_right = pygame.event.custom_type()

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == screen_update:
                fallen.draw(screen)
                tetrimino.draw(screen)
                pygame.display.flip()
            if event.type == block_fall:
                collided = tetrimino.update(fallen)
                if collided:
                    fallen.add(tetrimino.sprites())
                    tetrimino.empty()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    pygame.time.set_timer(auto_repeat_right, AUTO_REPEAT_TIME, loops=1)
                    tetrimino.move(1, fallen)
                elif event.key == K_LEFT:
                    pygame.time.set_timer(auto_repeat_left, AUTO_REPEAT_TIME, loops=1)
                    tetrimino.move(-1, fallen)
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    pygame.time.set_timer(auto_repeat_right, 0)
                    pygame.time.set_timer(move_right, 0)
                elif event.key == K_LEFT:
                    pygame.time.set_timer(auto_repeat_left, 0)
                    pygame.time.set_timer(move_left, 0)
            if event.type == auto_repeat_right:
                pygame.time.set_timer(move_right, AUTO_REPEAT_SPEED)
            if event.type == auto_repeat_left:
                pygame.time.set_timer(move_left, AUTO_REPEAT_SPEED)
            if event.type == move_right:
                tetrimino.move(1, fallen)
            if event.type == move_left:
                tetrimino.move(-1, fallen)

if __name__ == "__main__":
    main()