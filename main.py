import sys
from collections import OrderedDict

import pygame
from pygame.locals import *

import events
from game import Game
from block import Block, Tetrimino, Fallen
from timer import Timer
from debug import Debug
from settings import *

### TODO:
###
### Hard Drop
### Lock Down
### Show queue
### Losing
### Sound

class Drawer:
    def __init__(self, screen):
        self.screen = screen
        self.sprites = OrderedDict() # {z: [sprites]}
    
    def add(self, *sprites, z=0):
        if z not in self.sprites:
            self.sprites[z] = []
        self.sprites[z].extend(sprites)
        self.sprites = OrderedDict((zz, self.sprites[zz]) for zz in sorted(self.sprites))
    
    def remove(self, sprite):
        for z in self.sprites:
            if sprite in self.sprites[z]:
                self.sprites[z].remove(sprite)
                break
    
    def draw(self):
        for z in self.sprites:
            for sprite in self.sprites[z]:
                self.screen.blit(sprite.image, sprite.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    debug = Debug(screen, (50, 50))

    event_manager = events.EventManager()
    loop_id = event_manager.register()
    event_manager.subscribe(loop_id, events.screen_update)
    event_manager.subscribe(loop_id, QUIT)
    event_manager.subscribe(loop_id, KEYDOWN)

    timer = Timer(event_manager)
    drawer = Drawer(screen)
    timer.set_timer(events.screen_update, int(1000/60))

    game = Game(drawer, timer, event_manager)
    game.start()

    while True:
        timer.tick()
        event_manager.push(*pygame.event.get())
        game.update()

        for event in event_manager.get(loop_id):
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == events.screen_update:
                drawer.draw()
                pygame.display.flip()

def _main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    debug = Debug(screen, (50, 50))
    timer = Timer()
    drawer = Drawer(screen)

    background = pygame.image.load("background.png")
    background = background.convert()
    bg_sprite = pygame.sprite.Sprite()
    bg_sprite.image = background
    bg_sprite.rect = pygame.rect.Rect((0, 0), SCREEN_SIZE)
    drawer.add(bg_sprite, z=-1)

    queue = []
    fallen = Fallen()
    drawer.add(*fallen.sprites())

    falling_fast = False
    timer.set_timer(events.screen_update, int(1000/60))    

    def place_tetrimino():
        tetrimino = queue.pop()
        if len(queue) == 0:
            new_queue()
        tetrimino.place()
        drawer.add(*tetrimino.sprites())
        timer.set_timer(events.block_fall, BLOCK_FALL_FAST_TIME if falling_fast else BLOCK_FALL_TIME, delay=BLOCK_FALL_DELAY, pause=True)
        return tetrimino
    
    def new_queue():
        for shape in random.sample(range(7), 7):
            queue.append(Tetrimino(shape))

    new_queue()
    tetrimino = place_tetrimino()

    while True:
        timer.tick()

        screen.blit(background, (0, 0))
        debug.blit()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == events.screen_update:
                drawer.draw()
                pygame.display.flip()
            if event.type == events.block_fall:
                collided = tetrimino.move((0,1), fallen)
                if collided:
                    for block in tetrimino.sprites():
                        fallen.add_block(block)
                    completed_lines = fallen.check_lines()
                    if len(completed_lines) > 0:
                        timer.pause()
                        timer.set_timer(events.clear_lines, 200, loops=1)
                        fallen.paint_lines()
                    else:
                        tetrimino = place_tetrimino()
            if event.type == events.clear_lines:
                for j in fallen.check_lines():
                    [drawer.remove(block) for block in fallen.get_row(j)]
                fallen.clear_lines()
                tetrimino = place_tetrimino()
                timer.unpause()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_p:
                    timer.paused = not timer.paused
                if not timer.paused:
                    if event.key == K_RIGHT:
                        timer.set_timer(events.move_right, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY, pause=True)
                        tetrimino.move((1,0), fallen)
                    elif event.key == K_LEFT:
                        timer.set_timer(events.move_left, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY, pause=True)
                        tetrimino.move((-1,0), fallen)
                    elif event.key == K_DOWN:
                        falling_fast = True
                        timer.set_timer(events.block_fall, BLOCK_FALL_FAST_TIME, pause=True)
                    elif event.key == CW_KEY or event.key == CCW_KEY:
                        tetrimino.rotate(event.key, fallen)
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    timer.set_timer(events.move_right, 0)
                elif event.key == K_LEFT:
                    timer.set_timer(events.move_left, 0)
                elif event.key == K_DOWN:
                    falling_fast = False
                    timer.set_timer(events.block_fall, BLOCK_FALL_TIME, pause=True)
            if event.type == events.move_right:
                tetrimino.move((1,0), fallen)
            if event.type == events.move_left:
                tetrimino.move((-1,0), fallen)
        
if __name__ == "__main__":
    print(f"Dev mode: {sys.flags.dev_mode}")
    main()