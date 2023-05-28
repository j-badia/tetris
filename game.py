import random
import pygame
import events
from block import Tetrimino, Fallen
from settings import *

class Game:
    bg_image = None
    next_font = None

    @classmethod
    def load_bg(cls):
        if cls.bg_image is None:
            cls.bg_image = pygame.image.load("background.png").convert()

    @classmethod
    def create_font(cls):
        if cls.next_font is None:
            pygame.font.init()
            cls.next_font = pygame.font.SysFont(NEXT_FONT, NEXT_FONTSIZE, bold=True)

    def __init__(self, drawer, event_manager):
        self.drawer = drawer
        self.event_manager = event_manager
        self.id = self.event_manager.register()
        self.event_manager.subscribe(self.id,
                                     events.block_fall,
                                     events.clear_lines,
                                     events.move_left,
                                     events.move_right,
                                     pygame.KEYDOWN,
                                     pygame.KEYUP)

        self.load_bg()
        background = pygame.sprite.Sprite()
        background.image = self.bg_image
        background.rect = pygame.rect.Rect((0, 0), SCREEN_SIZE)
        self.drawer.add(background, z=-1)

        self.create_font()
        next = pygame.sprite.Sprite()
        next.image = self.next_font.render("NEXT", True, (230, 230, 230))
        next.rect = next.image.get_rect()
        next.rect.centerx = MATRIX_CORNER_POS[0] + BLOCK_SIZE*NEXT_POS[0]
        next.rect.bottom = MATRIX_CORNER_POS[1] + BLOCK_SIZE*(NEXT_POS[1]-2)
        self.drawer.add(next)

        self.queue = []
        self.fallen = Fallen()
        self.drawer.add(*self.fallen.sprites())
        self.falling_fast = False
    
    def place_tetrimino(self):
        if len(self.queue) < 2:
            self.new_queue()
        self.tetrimino = self.next_tetrimino
        self.next_tetrimino = self.queue.pop()
        self.tetrimino.place()
        self.next_tetrimino.place(center=NEXT_POS)
        self.drawer.add(*self.next_tetrimino.sprites())
        if self.tetrimino.test_collision(self.fallen):
            self.event_manager.set_timer(events.lost, LOSE_DELAY, loops=1)
            self.event_manager.set_timer(events.block_fall, 0)
        else:
            time = BLOCK_FALL_FAST_TIME if self.falling_fast else BLOCK_FALL_TIME
            self.event_manager.set_timer(events.block_fall, time, delay=BLOCK_FALL_DELAY)

    def new_queue(self):
        for shape in random.sample(range(7), 7):
            self.queue.append(Tetrimino(shape))
    
    def start(self):
        self.queue = []
        self.new_queue()
        self.next_tetrimino = self.queue.pop()
        self.drawer.add(*self.next_tetrimino.sprites())
        self.place_tetrimino()
    
    def end(self):
        for block in self.fallen.sprites():
            self.drawer.remove(block)
        for block in self.tetrimino.sprites():
            self.drawer.remove(block)
        for block in self.next_tetrimino.sprites():
            self.drawer.remove(block)
        self.event_manager.deregister(self.id)
    
    def update(self):
        for event in self.event_manager.get(self.id):
            moved = False
            if event.type == events.block_fall:
                if self.falling_fast:
                    moved = True
                collided = self.tetrimino.move((0,1), self.fallen)
                if collided:
                    self.event_manager.push(pygame.event.Event(events.play_sound, {"name": "block-lock"}))
                    if max(block.mat_pos[1] for block in self.tetrimino.sprites()) < 0:
                        self.event_manager.set_timer(events.lost, LOSE_DELAY, loops=1)
                    else:
                        for block in self.tetrimino.sprites():
                            self.fallen.add_block(block)
                        self.fallen.check_lines()
                        if len(self.fallen.completed_lines) > 0:
                            self.event_manager.set_timer(events.block_fall, 0)
                            self.event_manager.set_timer(events.clear_lines, LINE_CLEAR_DELAY, loops=1)
                            self.fallen.paint_lines()
                        else:
                            self.place_tetrimino()
            elif event.type == events.clear_lines:
                for j in self.fallen.completed_lines:
                    [self.drawer.remove(block) for block in self.fallen.get_row(j)]
                self.fallen.clear_lines()
                self.place_tetrimino()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.event_manager.set_timer(events.move_right, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY)
                    self.tetrimino.move((1,0), self.fallen)
                    moved = True
                elif event.key == pygame.K_LEFT:
                    self.event_manager.set_timer(events.move_left, AUTO_REPEAT_TIME, delay=AUTO_REPEAT_DELAY)
                    self.tetrimino.move((-1,0), self.fallen)
                    moved = True
                elif event.key == pygame.K_DOWN:
                    self.falling_fast = True
                    self.event_manager.set_timer(events.block_fall, BLOCK_FALL_FAST_TIME)
                elif event.key in CW_KEYS or event.key in CCW_KEYS:
                    self.tetrimino.rotate(event.key, self.fallen)
                    self.event_manager.push(pygame.event.Event(events.play_sound, {"name": "block-rotate"}))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.event_manager.set_timer(events.move_right, 0)
                elif event.key == pygame.K_LEFT:
                    self.event_manager.set_timer(events.move_left, 0)
                elif event.key == pygame.K_DOWN:
                    self.falling_fast = False
                    self.event_manager.set_timer(events.block_fall, BLOCK_FALL_TIME)
            elif event.type == events.move_right:
                self.tetrimino.move((1,0), self.fallen)
                moved = True
            elif event.type == events.move_left:
                self.tetrimino.move((-1,0), self.fallen)
                moved = True
            if moved:
                self.event_manager.push(pygame.event.Event(events.play_sound, {"name": "block-move"}))