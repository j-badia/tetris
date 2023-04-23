import random, sys
import pygame
from pygame.locals import *
from settings import *
from block import Block, Tetrimino, Fallen
from timer import Timer
from debug import Debug

### TODO:
###
### Hard Drop
### Lock Down
### Line clear
### Losing

def main():
    long_time = 0 #24*3600*1000 #Bug in set_timer(ev, 0)

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    debug = Debug(screen, (50, 50))
    timer = Timer()

    background = pygame.image.load("background.png")
    background = background.convert()

    queue = []
    fallen = Fallen()
    matrix = [MATRIX_SIZE[0]*[0] for i in range(MATRIX_SIZE[1])]

    screen_update = pygame.event.custom_type()
    block_fall_start = pygame.event.custom_type()
    block_fall = pygame.event.custom_type()
    falling_fast = False
    timer.set_timer(screen_update, int(1000/60))
    #timer.set_timer(block_fall, 500)

    auto_repeat_left = pygame.event.custom_type()
    auto_repeat_right = pygame.event.custom_type()
    move_left = pygame.event.custom_type()
    move_right = pygame.event.custom_type()

    def place_tetrimino():
        tetrimino = queue.pop()
        tetrimino.place()
        timer.set_timer(block_fall_start, BLOCK_FALL_DELAY, loops=1)
        timer.set_timer(block_fall, long_time)
        return tetrimino
    
    def new_queue():
        for shape in random.sample(range(7), 7):
            queue.append(Tetrimino(shape))

    new_queue()
    tetrimino = place_tetrimino()

    while True:
        timer.tick()
        if len(queue) == 0:
            new_queue()

        screen.blit(background, (0, 0))
        debug.blit()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == screen_update:
                fallen.draw(screen)
                tetrimino.draw(screen)
                pygame.display.flip()
            if event.type == block_fall_start:
                time = BLOCK_FALL_FAST_TIME if falling_fast else BLOCK_FALL_TIME
                timer.set_timer(block_fall, time)
            if event.type == block_fall:
                collided = tetrimino.move((0,1), fallen.sprites())
                if collided:
                    for block in tetrimino.sprites():
                        fallen.add_block(block)
                    completed_lines = []
                    for j in reversed(range(MATRIX_SIZE[1])):
                        complete_line = True
                        for elem in fallen.get_row(j):
                            if elem is None:
                                complete_line = False
                        if complete_line:
                            completed_lines.append(j)
                            for i in range(MATRIX_SIZE[0]):
                                fallen.get(i, j).image.fill((230, 230, 230))
                    if len(completed_lines) > 0:
                        pygame.time.delay(500)
                        fallen.clear(completed_lines)
                    tetrimino = place_tetrimino()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    timer.set_timer(auto_repeat_right, AUTO_REPEAT_DELAY, loops=1)
                    tetrimino.move((1,0), fallen)
                elif event.key == K_LEFT:
                    timer.set_timer(auto_repeat_left, AUTO_REPEAT_DELAY, loops=1)
                    tetrimino.move((-1,0), fallen)
                elif event.key == K_DOWN:
                    falling_fast = True
                    timer.set_timer(block_fall, BLOCK_FALL_FAST_TIME)
                elif event.key == CW_KEY or event.key == CCW_KEY:
                    tetrimino.rotate(event.key, fallen)
                elif event.key == K_ESCAPE:
                    return
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    timer.set_timer(auto_repeat_right, long_time)
                    timer.set_timer(move_right, long_time)
                elif event.key == K_LEFT:
                    timer.set_timer(auto_repeat_left, long_time)
                    timer.set_timer(move_left, long_time)
                elif event.key == K_DOWN:
                    falling_fast = False
                    timer.set_timer(block_fall, BLOCK_FALL_TIME)
            if event.type == auto_repeat_right:
                timer.set_timer(move_right, AUTO_REPEAT_TIME)
            if event.type == auto_repeat_left:
                timer.set_timer(move_left, AUTO_REPEAT_TIME)
            if event.type == move_right:
                tetrimino.move((1,0), fallen)
            if event.type == move_left:
                tetrimino.move((-1,0), fallen)
        
if __name__ == "__main__":
    print(f"Dev mode: {sys.flags.dev_mode}")
    main()