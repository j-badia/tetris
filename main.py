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
### Levels / speed change

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
        self.event_manager.subscribe(self.id,
                                     events.play_sound,
                                     events.pause_audio,
                                     events.unpause_audio,
                                     events.start_music_intro,
                                     events.start_music_transition,
                                     events.start_music_main)
        self.sounds = {}
        self.loops = set()
        self.enabled = True
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
        for sound in self.sounds:
            sound.stop()
    
    def pause(self):
        pygame.mixer.pause()
    
    def unpause(self):
        pygame.mixer.unpause()
    
    def load(self, name, file, volume=1):
        self.sounds[name] = pygame.mixer.Sound(file=SOUNDS_FOLDER+file)
        self.sounds[name].set_volume(volume)
    
    def play(self, name, volume=1):
        channel = self.sounds[name].play()
        channel.set_volume(volume)
        return channel
    
    def stop(self, name):
            self.sounds[name].stop()
    
    def stop_channel(self, channel):
        channel.stop()
    
    def loop(self, name, volume=1):
        channel = self.play(name, volume)
        self.loops.add(channel)
        return channel
    
    def stop_loop(self, channel):
        self.loops.remove(channel)
    
    def update(self):
        if self.enabled:
            for channel in self.loops:
                if channel.get_queue() is None:
                    channel.queue(channel.get_sound())
        for event in self.event_manager.get(self.id):
            if not self.enabled:
                continue
            if event.type == events.play_sound:
                if hasattr(event, "volume"):
                    volume = event.volume
                else:
                    volume = 1
                self.play(event.name, volume)
            elif event.type == events.pause_audio:
                self.pause()
            elif event.type == events.unpause_audio:
                self.unpause()
            elif event.type == events.start_music_intro:
                self.music_channel = self.loop("music-intro")
            elif event.type == events.start_music_transition:
                self.stop_loop(self.music_channel)
                self.music_channel.set_endevent(events.start_music_main)
                self.music_channel.queue(self.sounds["music-transition"])
            elif event.type == events.start_music_main:
                self.music_channel.queue(self.sounds["music-main"])
                self.loops.add(self.music_channel)

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
    audio.load("music-intro", "music-intro.ogg", 0.4)
    audio.load("music-main", "music-main.ogg", 0.4)
    audio.load("music-transition", "music-transition.ogg", 0.4)
    audio.load("menu-select", "go.wav", 0.2)
    audio.load("block-move", "lock.wav", 0.05)
    audio.load("block-lock", "move.wav", 0.15)
    audio.load("block-rotate", "ma_sfx_rotate.wav", 0.2)
    for i in range(1, 5):
        audio.load(f"combo{i}", f"combo{i}.wav", 0.2)

    game_state = GameState(drawer, event_manager)

    debug = Debug(screen, (50, 50))
    drawer.add(debug, z=10)

    while True:
        timer.tick()
        event_manager.push(*pygame.event.get())
        audio.update()
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