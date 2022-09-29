import pygame, pymunk, sys

import scene
from base import *
from gui import *
from item import *
from myobject import *

class Game:
    window_size = 800, 450
    window_ratio = window_size[0]/window_size[1]
    color_bit = 8
    window_caption = {
        'main': 'shogun game', 
        '': '',
        'pause': '', 
        }
    max_fps = 60
    step_per_frame = .135 * 60/max_fps
    step_hz = 20
    step_dt = step_per_frame/step_hz
    
    # init variable
    def __init__(self): 
        self.init()
        self.timer = pygame.time.Clock()
        self.input_respone = {
            pygame.QUIT: self.exit,
            pygame.WINDOWFOCUSLOST: self.pause,
            pygame.WINDOWRESIZED: self.resize,
            }
        self.window = pygame.display.set_mode(
            size=self.window_size,
            depth=self.color_bit * 4
            )
        self.scene = {cls.__name__ : cls(self) for cls in scene} # test 
        self.current_scene = self.scene['menu']     
    
    # init class
    def init(self): 
        pygame.init()
        j = json_to_dict('Attribute.json')
        for clsname, instance_group in j.items():
            cls = globals()[clsname]
            info = {name: cls(**attr) for name, attr in instance_group.items()}
            setattr(self, clsname.lower, info)
            
    def pause(self):
        self.current_scene.pause()
        
    def exit(self):
        confirm = self.current_scene.exit()
        if confirm: sys.exit()
    
    def resize(self):
        self.pause()
        
    def goto(self, sc):
        self.current_scene.leave()
        self.current_scene = self.scene[sc]
        self.current_scene()
    
    def handle_input(self):
        self.key = pygame.key.get_pressed()
        for event in pygame.event.get():
            respone_func = self.input_respone.get(event.type, None)
            if respone_func is not None: respone_func(event)        
    
    def run(self):
        try: 
            while 1: 
                self.handle_input()
                self.current_scene.respone()
                self.current_scene.draw()
                self.timer.tick(self.max_fps)
        finally: 
            pygame.quit()

if __name__ == '__main__':
    mygame = Game()
    mygame.run()
    # assert x > 0, 'if false print this'