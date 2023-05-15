from collections import defaultdict
import pygame

class EventManager:
    def __init__(self):
        self.subscribed = defaultdict(list) # {ev_type: [sub_ids]}
        self.queues = {} # {sub_id: [evs]}
        self.last_id = 0
    
    def register(self):
        self.last_id += 1
        self.queues[self.last_id] = []
        return self.last_id
    
    def subscribe(self, sub_id, *event_types):
        for event_type in event_types:
            self.subscribed[event_type].append(sub_id)
    
    def unsubscribe(self, sub_id, *event_types):
        for event_type in event_types:
            if event_type in self.subscribed:
                del self.subscribed[event_type]
        self.queues[sub_id] = [event for event in self.queues[sub_id] if event.type not in event_types]
    
    def push(self, *events):
        for event in events:
            for sub in self.subscribed[event.type]:
                self.queues[sub].append(event)
    
    def get(self, sub_id):
        event = self.get_next(sub_id)
        if event is not None:
            yield event
    
    def get_next(self, sub_id):
        if sub_id in self.queues and len(self.queues[sub_id]) > 0:
            return self.queues[sub_id].pop(0)
        return None

screen_update = pygame.event.custom_type()

pause = pygame.event.custom_type()

block_fall = pygame.event.custom_type()
clear_lines = pygame.event.custom_type()
move_left = pygame.event.custom_type()
move_right = pygame.event.custom_type()