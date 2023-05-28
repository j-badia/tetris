import pygame
import events
from settings import *

class CenteredText(pygame.sprite.Sprite):
    font = None

    @classmethod
    def create_font(cls):
        if cls.font is None:
            pygame.font.init()
            cls.font = pygame.font.SysFont(MENU_OPT_FONT, MENU_OPT_FONTSIZE, bold=True)

    def __init__(self, text):
        super().__init__()
        self.create_font()
        self.image_normal = self.font.render(text, True, (230, 230, 230))
        self.image_highlight = self.font.render(text, True, (120, 190, 250))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.move_ip(SCREEN_SIZE[0]/2 - self.rect.width/2, 0)
    
    def highlight(self):
        self.image = self.image_highlight
    
    def reset_highlight(self):
        self.image = self.image_normal

class Options(pygame.sprite.Group):
    def __init__(self, options, commands):
        super().__init__()
        self.options = [] # For compatibility in versions where sprites aren't ordered
        self.commands = commands
        n = len(options)
        self.heights = [SCREEN_SIZE[1]/2 + (i-n/2)*MENU_OPT_SEPARATION for i in range(n)]
        for text, height in zip(options, self.heights):
            option = CenteredText(text)
            option.rect.centery = height
            self.add(option)
            self.options.append(option)

class Cursor(pygame.sprite.Sprite):
    image = None

    @classmethod
    def load(cls):
        if cls.image is None:
            cls.image = pygame.image.load("cursor.png").convert()

    def __init__(self, options):
        super().__init__()
        self.load()
        self.n = len(options)
        self.options = options
        self.heights = self.options.heights
        self.rights = [option.rect.left-CURSOR_SEPARATION for option in self.options]

        self.rect = self.image.get_rect()
        self.place(0)
    
    def place(self, pos):
        self.pos = pos
        self.rect.centery = self.heights[self.pos]
        self.rect.right = self.rights[self.pos]

    def move_up(self):
        self.place((self.pos-1) % self.n)
    
    def move_down(self):
        self.place((self.pos+1) % self.n)

class Menu:
    def __init__(self, options, commands, drawer, event_manager):
        self.drawer = drawer
        self.event_manager = event_manager
        self.id = event_manager.register()
        self.event_manager.subscribe(self.id, pygame.KEYDOWN)

        self.event_manager.subscribe(self.id,
                                     events.option_selected)

        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface(SCREEN_SIZE)
        self.background.image.set_alpha(MENU_BG_ALPHA)
        self.background.rect = pygame.rect.Rect((0,0), SCREEN_SIZE)
        self.drawer.add(self.background, z=1)

        self.options = Options(options, commands)
        self.drawer.add(*self.options.sprites(), z=2)

        self.cursor = Cursor(self.options)
        self.drawer.add(self.cursor, z=2)
    
    def update(self):
        for event in self.event_manager.get(self.id):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.cursor.move_up()
                elif event.key == pygame.K_DOWN:
                    self.cursor.move_down()
                elif event.key == pygame.K_RETURN:
                    pos = self.cursor.pos
                    self.options.options[pos].highlight()
                    command = self.options.commands[pos]
                    self.event_manager.set_timer(events.option_selected, SELECTION_DELAY, loops=1,
                                         ev_dict={"pos": pos, "command": command})
                    self.event_manager.push(pygame.event.Event(events.play_sound,
                                            {"name": "menu-select"}))

    def close(self):
        self.drawer.remove(self.background)
        for spr in self.options.sprites():
            self.drawer.remove(spr)
        self.drawer.remove(self.cursor)