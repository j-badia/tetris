import random
import pygame
import events
from block import Tetrimino, Fallen
from settings import *

class Game:
    def __init__(self, drawer, timer, event_manager):
        self.drawer = drawer
        self.timer = timer
        self.event_manager = event_manager
        self.id = self.event_manager.register()
        self.event_manager.subscribe(self.id,
                                     events.block_fall,
                                     events.clear_lines,
                                     events.move_left,
                                     events.move_right,
                                     KEYDOWN,
                                     KEYUP)

        background = pygame.sprite.Sprite()
        background.image = pygame.image.load("background.png").convert()
        background.rect = pygame.rect.Rect((0, 0), SCREEN_SIZE)
        self.drawer.add(background, z=-1)

        self.queue = []
        self.fallen = Fallen()
        self.drawer.add(*self.fallen.sprites())
        self.falling_fast = False
    
    def place_tetrimino(self):
        self.tetrimino = self.queue.pop()
        if len(self.queue) == 0:
            self.new_queue()
        self.tetrimino.place()
        self.drawer.add(*self.tetrimino.sprites())
        time = BLOCK_FALL_FAST_TIME if self.falling_fast else BLOCK_FALL_TIME
        self.timer.set_timer(events.block_fall, time, delay=BLOCK_FALL_DELAY)

    def new_queue(self):
        for shape in random.sample(range(7), 7):
            self.queue.append(Tetrimino(shape))
    
    def start(self):
        self.new_queue()
        self.place_tetrimino()
    
    def end(self):
        for block in self.fallen.sprites():
            self.drawer.remove(block)
        for block in self.tetrimino.sprites():
            self.drawer.remove(block)
    
    def update(self):
        for event in self.event_manager.get(self.id):
            if event.type == events.block_fall:
                collided = self.tetrimino.move((0,1), self.fallen)
                if collided:
                    for block in self.tetrimino.sprites():
                        self.fallen.add_block(block)
                    self.fallen.check_lines()
                    if len(self.fallen.completed_lines) > 0:
                        self.timer.set_timer(events.block_fall, 0)
                        self.timer.set_timer(events.clear_lines, LINE_CLEAR_DELAY, loops=1)
                        self.fallen.paint_lines()
                    else:
                        self.place_tetrimino()
            elif event.type == events.clear_lines:
                for j in self.fallen.completed_lines:
                    [self.drawer.remove(block) for block in self.fallen.get_row(j)]
                self.fallen.clear_lines()
                self.place_tetrimino()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #self.event_manager.push(events.pause)
                    pass
                elif event.key == K_RIGHT:
                    self.timer.set_timer(events.move_right, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY)
                    self.tetrimino.move((1,0), self.fallen)
                elif event.key == K_LEFT:
                    self.timer.set_timer(events.move_left, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY)
                    self.tetrimino.move((-1,0), self.fallen)
                elif event.key == K_DOWN:
                    self.falling_fast = True
                    self.timer.set_timer(events.block_fall, BLOCK_FALL_FAST_TIME)
                elif event.key == CW_KEY or event.key == CCW_KEY:
                    self.tetrimino.rotate(event.key, self.fallen)
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.timer.set_timer(events.move_right, 0)
                elif event.key == K_LEFT:
                    self.timer.set_timer(events.move_left, 0)
                elif event.key == K_DOWN:
                    self.falling_fast = False
                    self.timer.set_timer(events.block_fall, BLOCK_FALL_TIME, pause=True)
            elif event.type == events.move_right:
                self.tetrimino.move((1,0), self.fallen)
            elif event.type == events.move_left:
                self.tetrimino.move((-1,0), self.fallen)