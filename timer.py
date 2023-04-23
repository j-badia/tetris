import pygame
from pygame.time import get_ticks

# timers[eventid] : [event, time, last_tick, loops, delay]
class Timer:
    def __init__(self):
        self.timers = {}
    
    def set_timer(self, eventid, time, loops=0, delay=0):
        if time == 0:
            if eventid in self.timers:
                del self.timers[eventid]
        else:
            self.timers[eventid] = [pygame.event.Event(eventid), time, get_ticks(), loops, delay]
    
    def tick(self):
        tick = get_ticks()
        to_delete = []
        for eventid, (event, time, last_tick, loops, delay) in self.timers.items():
            if delay > 0:
                if tick - last_tick > delay:
                    self.timers[eventid][4] = 0
                    self.timers[eventid][2] = tick
            else:
                if tick - last_tick > time:
                    pygame.event.post(event)
                    self.timers[eventid][2] = tick
                    if loops != 0:
                        if loops == 1:
                            to_delete.append(eventid)
                        else:
                            self.timers[eventid][3] -= 1
        for eventid in to_delete:
            del self.timers[eventid]