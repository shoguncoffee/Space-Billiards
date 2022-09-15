import pygame
import pymunk, sys
from base import raiser

import scene
from base import *
from gui import *
from item import *
from myobject import *
from scene import menu

class Game:
    window_size = 800, 450
    color_bit = 8
    window_caption = ['shogun game', '', '']
    gravity = 700
    max_fps = 50
    dt = 1/max_fps
    
    def __init__(self):
        pygame.init()
        self.init()
        self.timer = pygame.time.Clock()
        
        self.input_respone = {
            pygame.QUIT: self.exit,
            pygame.WINDOWFOCUSLOST: self.pause,
            pygame.WINDOWRESIZED: self.pause
            }
        self.window = pygame.display.set_mode(
            size=self.window_size,
            depth=self.color_bit*4
            )
        self.scene = {cls.__name__ : cls(self) for cls in scene} # test   
        
        self.space = pymunk.Space()
        self.space.gravity = 0, -self.gravity
        self.draw_option = pymunk.pygame_util.DrawOptions(self.window)
        
        self.goto('menu')
        self.run()
    
    def init(self):
        dataclass = Character, Weapon, Text
        f = json_to_dict(f'{classname}_attribute.json')
        for cls in dataclass:
            classname = cls.__name__
            data = f[classname]
            info = {name: cls(**attr) for name, attr in data.items()}
            setattr(self, classname, info)    
            
    def pause(self):
        self.current_scene.pause()
        self.window_caption[1] = '(pause)'
        
    def exit(self):
        self.current_scene.exit()
        sys.exit()
        
    def goto(self, sc):
        self.current_scene.on_leave()
        self.current_scene = self.scene[sc]
         
    def draw(self):
        self.space.step(self.dt)
        self.space.debug_draw(self.draw_option)
        # self.window.fill()
        pygame.display.update()
        pygame.display.set_caption(' '.join(self.window_caption))
        # getcaption = pygame.display.get_caption()[0]
    
    
    def handle_input(self):
        self.press_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            respone_func = self.input_respone.get(event.type, lambda k: None)
            respone_func(event)        
    
    def run(self):
        try: 
            while 1: 
                self.handle_input()
                self.current_scene.respone()
                self.draw()
                self.timer.tick(self.max_fps)
        finally: 
            pygame.quit()

if __name__ == '__main__':
    Game()
    # assert x > 0, 'if false print this'