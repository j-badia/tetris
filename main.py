import sys
from collections import OrderedDict
import pygame

import events
from gamestate import GameState
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

class Audio:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.id = self.event_manager.register()
        self.event_manager.subscribe(self.id, events.play_sound)
        self.sounds = {}
    
    def load(self, name, file, volume=1):
        self.sounds[name] = pygame.mixer.Sound(file=file)
        self.sounds[name].set_volume(volume)
    
    def update(self):
        for event in self.event_manager.get(self.id):
            if event.type == events.play_sound:
                name = event.name
                if hasattr(event, "loops"):
                    loops = event.loops
                else:
                    loops = 0
                channel = self.sounds[name].play(loops=loops)
                if hasattr(event, "volume"):
                    channel.set_volume(event.volume)
                else:
                    channel.set_volume(1)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    timer = Timer()
    event_manager = events.EventManager(timer)
    loop_id = event_manager.register()
    event_manager.subscribe(loop_id, events.screen_update)
    event_manager.subscribe(loop_id, pygame.QUIT)
    event_manager.set_timer(events.screen_update, int(1000/60))

    drawer = Drawer(screen)
    audio = Audio(event_manager)
    #audio.load("bg music", "theme-lofi.ogg", 0)

    game_state = GameState(drawer, event_manager)

    bg_music = pygame.mixer.Sound(file="theme-lofi.mp3")
    bg_music.play(loops=-1)
    debug = Debug(screen, (50, 50))
    drawer.add(debug, z=10)

    while True:
        timer.tick()
        event_manager.push(*pygame.event.get())
        game_state.update()
        audio.update()

        for event in event_manager.get(loop_id):
            if event.type == pygame.QUIT:
                return
            elif event.type == events.screen_update:
                drawer.draw()
                pygame.display.flip()
        
if __name__ == "__main__":
    print(f"Dev mode: {sys.flags.dev_mode}")
    main()