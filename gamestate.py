from enum import Enum, auto
import pygame

import events
from menu import Menu
from game import Game

class MenuCommand(Enum):
    new_game = auto()
    resume = auto()
    quit = auto()

class State(Enum):
    start = auto()
    game = auto()
    paused = auto()
    lost = auto()

class GameState:
    def __init__(self, drawer, event_manager):
        self.drawer = drawer
        self.event_manager = event_manager
        self.id = self.event_manager.register()
        self.event_manager.subscribe(self.id,
                                     events.option_selected,
                                     events.lost,
                                     pygame.KEYDOWN)
        self.state = State.start
        self.scene = Menu(("NEW GAME", "QUIT"),
                          (MenuCommand.new_game, MenuCommand.quit),
                           self.drawer, self.event_manager)
        self.event_manager.push(pygame.event.Event(events.start_music_intro))
    
    def new_game(self):
        self.game = Game(self.drawer, self.event_manager)
        self.scene = self.game
        self.game.start()

    def update(self):
        self.scene.update()
        for event in self.event_manager.get(self.id):
            if self.state == State.start:
                if event.type == events.option_selected:
                    if event.command == MenuCommand.quit:
                        self.event_manager.push(pygame.event.Event(pygame.QUIT))
                    elif event.command == MenuCommand.new_game:
                        self.state = State.game
                        self.scene.close()
                        self.new_game()
                        self.event_manager.push(pygame.event.Event(events.start_music_transition))
            elif self.state == State.game:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = State.paused
                    self.event_manager.pause(self.game.id)
                    self.event_manager.push(pygame.event.Event(events.pause_audio))
                    self.scene = Menu(("RESUME", "NEW GAME", "QUIT"),
                                      (MenuCommand.resume, MenuCommand.new_game, MenuCommand.quit),
                                      self.drawer, self.event_manager)
                elif event.type == events.lost:
                    self.state = State.lost
                    self.event_manager.pause(self.game.id)
                    self.scene = Menu(("NEW GAME", "QUIT"),
                                      (MenuCommand.new_game, MenuCommand.quit),
                                    self.drawer, self.event_manager)
            elif self.state == State.paused:
                if event.type == events.option_selected:
                    if event.command == MenuCommand.quit:
                        self.event_manager.push(pygame.event.Event(pygame.QUIT))
                    elif event.command == MenuCommand.resume:
                        self.state = State.game
                        self.scene.close()
                        self.event_manager.unpause(self.game.id)
                        self.event_manager.push(pygame.event.Event(events.unpause_audio))
                        self.scene = self.game
                    elif event.command == MenuCommand.new_game:
                        self.state = State.game
                        self.scene.close()
                        self.game.end()
                        self.event_manager.push(pygame.event.Event(events.unpause_audio))
                        self.new_game()
            elif self.state == State.lost:
                if event.type == events.option_selected:
                    if event.command == MenuCommand.quit:
                        self.event_manager.push(pygame.event.Event(pygame.QUIT))
                    elif event.command == MenuCommand.new_game:
                        self.state = State.game
                        self.scene.close()
                        self.game.end()
                        self.new_game()