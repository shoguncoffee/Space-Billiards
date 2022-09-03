import pygame, sys
import random, json
import tqdm
import pymunk
from pygame.locals import *

from gui import *
from myobject import *
from item import *    

class Game:
    window_size = 600, 600
    color_bit = 8
    window_caption = 'shogun game'

    def __init__(self):
        self.timer = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            depth=self.color_bit*4
            )
        pygame.display.set_caption(self.window_caption)
        self.init_object()
        
    def handle_externalEvent():
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
    def run(self):
        self.sc_menu()
        while 1:
            self.handle_externalEvent()
            self.operate()
            pygame.display.update()
            self.timer.tick(60)
    
    def init_object(self): 
        charcter_info = open('character_attribute.json')
        json.load()
        self.character = {
            name: Character(f'{name}.png', **attr) for name, attr in charcter_info
            }
    
    class sc_menu:
        def __init__(self):
            self.screen.blits(
                (),
                (),
                (),
                ()
                )
            
            self.operate = self.updater()
            
        def updater():
            pass
    
    class sc_level:
        def __init__(self):
            self.screen.blits(
                (),
                (),
                (),
                ()
                )
            
            self.operate = self.updater()
            
        def updater():
            pass
    
if __name__ == '__main__':
    Game.run()
    