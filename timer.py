import pygame
from pygame.time import get_ticks

# timers[eventid] : [event, time, last_tick, loops, delay, pause]
class Timer:
    def __init__(self):
        self.timers = {}
        self.paused = False
    
    def set_timer(self, eventid, time, loops=0, delay=0, pause=False, ev_dict={}):
        if time == 0:
            if eventid in self.timers:
                del self.timers[eventid]
        else:
            self.timers[eventid] = [pygame.event.Event(eventid, ev_dict), time, get_ticks(), loops, delay, pause]
    
    def tick(self):
        curr_tick = get_ticks()
        to_delete = []
        for eventid, (event, time, last_tick, loops, delay, pause) in self.timers.items():
            if pause and self.paused:
                continue
            if delay > 0:
                if curr_tick - last_tick > delay:
                    self.timers[eventid][4] = 0
                    self.timers[eventid][2] = curr_tick
            else:
                if curr_tick - last_tick > time:
                    pygame.event.post(event)
                    self.timers[eventid][2] = curr_tick
                    if loops != 0:
                        if loops == 1:
                            to_delete.append(eventid)
                        else:
                            self.timers[eventid][3] -= 1
        for eventid in to_delete:
            del self.timers[eventid]
    
    def pause(self):
        self.paused = True
        self.last_pause = get_ticks()
    
    def unpause(self):
        self.paused = False
        paused_time = get_ticks() - self.last_pause
        for eventid, (event, time, last_tick, loops, delay, pause) in self.timers.items():
            if pause:
                self.timers[eventid][2] += paused_time