from base import *
import pymunk
from pymunk import Transform as Camera
import pymunk.pygame_util

class _scene_:
    def __init__(this, self):
        this.self = self
        
    def respone(this):
        self = this.self
        if : 
            this.pause()
        this.on_respone()  
        
    def leave(this):
        self = this.self
        this.on_leave()
    
    def pause(this):
        self = this.self
        this.on_respone(this, self)
    
    def enter(this):
        self = this.self
        this.loading(this, self)
    
    def on_draw(this):
        pass
    
    def on_respone(this):
        pass    
    
    def on_leave(this):
        pass    
    
    def on_pause(this):
        pass
    
    def on_enter(this):
        pass
    

class menu(_scene_):
    def __init__(this, self):
        super().__init__(self)
    
    def load(self):
        background = self.screen.blit(
            
            )
        title = self.screen.blit(
            
            )
        option = self.screen.blits(
            (),
            (),
            (),
            ()
            )
    
    def on_respone(self):
    
        
        if in option:
            pass
        
    def platform_collition():
        pass
    
    def on_pause():
        pass


class _level_(_scene_):
    translate_speed = 20
    zoom_speed = 0.1
    gravity = 700
    dt = 0.01
    I = pymunk.Transform()
    
    def __init__(this, self):
        super().__init__(self)

        
    def on_enter(this):
        this.space = pymunk.Space()
        this.camera = Camera()
        this.space.gravity = 0, -this.gravity
        this.draw_option = pymunk.pygame_util.DrawOptions(this.self.window)
        this.zoom_speed = .04
        this.shift_speed = 10        
        
    def on_draw(this):
        this.space.step()
        this.space.debug_draw(this.draw_option)
        this.self.window.fill((0, 0, 0))    
        
    def on_leave(this):
        this.draw_options.transform = this.I
        
    def cameraman(this):
        self = this.self
        if this.player:
            scaling *= 1 + zoom_speed*(k['zoom in'] - k['zoom out'])
            translate = [t + q*this.shift_speed for q, t in zip((k['left'] - k['right'], k['up'] - k['down']), translate)]
            print(round(scaling, 3), translate)
            this.draw_options.transform = pymunk.Transform().translated(300, 300).scaled(scaling).translated(*translate).translated(-300, - 300)


class lv_1(_level_):
    def __init__(this, self):
        super().__init__(self)