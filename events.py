from collections import defaultdict
import pygame

class EventManager:
    def __init__(self, timer):
        self.timer = timer
        self.subscribed = defaultdict(list) # {ev_type: [sub_ids]}
        self.paused = []
        self.queues = {} # {sub_id: [evs]}
        self.last_id = 0
    
    def register(self):
        self.last_id += 1
        self.queues[self.last_id] = []
        return self.last_id

    def deregister(self, id):
        del self.queues[id]
        to_delete = []
        for event_type in self.subscribed:
            sub_ids = self.subscribed[event_type]
            if id in sub_ids:
                if len(sub_ids) > 1:
                    self.subscribed[event_type].remove(id)
                else:
                    to_delete.append(event_type)
        for event_type in to_delete:
            del self.subscribed[event_type]
    
    def subscribe(self, sub_id, *event_types):
        for event_type in event_types:
            self.subscribed[event_type].append(sub_id)
    
    def unsubscribe(self, sub_id, *event_types):
        for event_type in event_types:
            if event_type in self.subscribed:
                del self.subscribed[event_type]
        self.queues[sub_id] = [event for event in self.queues[sub_id] if event.type not in event_types]

    def pause(self, id):
        self.paused.append(id)
        self.queues[id] = []
    
    def unpause(self, id):
        self.paused.remove(id)
    
    def push(self, *events):
        for event in events:
            for sub in self.subscribed[event.type]:
                if sub not in self.paused:
                    self.queues[sub].append(event)
    
    def get(self, sub_id):
        event = self.get_next(sub_id)
        if event is not None:
            yield event
    
    def get_next(self, sub_id):
        if sub_id in self.queues and len(self.queues[sub_id]) > 0:
            return self.queues[sub_id].pop(0)
        return None
    
    def set_timer(self, eventid, time, loops=0, delay=0, ev_dict={}):
        self.timer.set_timer(eventid, time, loops=loops, delay=delay, ev_dict=ev_dict)

screen_update = pygame.event.custom_type()

play_sound = pygame.event.custom_type()

pause = pygame.event.custom_type()
option_selected = pygame.event.custom_type()
lost = pygame.event.custom_type()

block_fall = pygame.event.custom_type()
clear_lines = pygame.event.custom_type()
move_left = pygame.event.custom_type()
move_right = pygame.event.custom_type()