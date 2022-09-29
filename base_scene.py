from base import *
import pymunk

class Camera:
    def __init__(self, draw_option):
        self.option = draw_option
    
    def scaled(self, scale):
        self.option.transform = self.option.transform.scaled(scale)
        return self
    
    def shift(self, x=0, y=0):
        self.option.transform = self.option.transform.translated(x, y)
        return self


class __scene__:
    def __init__(this, self):
        this.self = self
        
    def __call__(this, *args, **kwds):
        this.enter()
        # set stardard attr
        
    def draw(this):
        self = this.self
        this.on_draw()
        pygame.display.set_caption(' '.join(self.window_caption))
        pygame.display.update()
        
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
        this.on_respone()
    
    def enter(this):
        self = this.self
        this.on_enter()
        
    def exit(this):
        self = this.self
        return this.on_exit()
    
    def on_draw(this): 
        ...
    def on_respone(this): 
        ...    
    def on_leave(this): 
        ...    
    def on_pause(this): 
        ...
    def on_enter(this): 
        ...
    def on_exit(this): 
        ...
    def on_call(this): 
        ...