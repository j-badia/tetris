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

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    debug = Debug(screen, (50, 50))

    event_manager = events.EventManager()
    loop_id = event_manager.register()
    event_manager.subscribe(loop_id, events.screen_update)
    event_manager.subscribe(loop_id, pygame.QUIT)
    #event_manager.subscribe(loop_id, KEYDOWN)

    timer = Timer(event_manager)
    drawer = Drawer(screen)
    timer.set_timer(events.screen_update, int(1000/60))

    #game = Game(drawer, timer, event_manager)
    #game.start()
    #testmenu = Menu(["RESUME", "NEW GAME", "QUIT"], drawer, timer, event_manager)
    game_state = GameState(drawer, timer, event_manager)

    while True:
        timer.tick()
        event_manager.push(*pygame.event.get())
        game_state.update()

        for event in event_manager.get(loop_id):
            if event.type == pygame.QUIT:
                return
            elif event.type == events.screen_update:
                drawer.draw()
                pygame.display.flip()
        
if __name__ == "__main__":
    print(f"Dev mode: {sys.flags.dev_mode}")
    main()