from base import *
import pymunk
import pymunk.pygame_util
import base_scene

class menu(__scene__):
    def __init__(this, self):
        super().__init__(self)
    
    def on_enter(self):
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


class _level_(__scene__):
    translate_speed = 20
    zoom_speed = 0.1
    gravity = 700
    dt = 0.01
    I = pymunk.Transform()
    
    def __init__(this, self):
        super().__init__(self)
        this.space = pymunk.Space()
        
    def on_call(this):
        this.keymap = {
            '': this.player.y,
            'a': this.
        }
        
    def on_enter(this):
        this.space = pymunk.Space()
        this.camera = Camera()
        this.space.gravity = 0, -this.gravity
        this.camera = Camera(this.draw_option)
        this.zoom_speed = .04
        this.shift_speed = 10        
        
    def on_draw(this):
        self = this.self
        for _ in range(self.step_hz): this.space.step(self.step_dt)
        this.self.window.fill((0, 0, 0))
        
    def on_leave(this):
        this.draw_options.transform = this.I
              
    def camera(this, scale, shift):
        self = this.self
        if this.player:
            scaling *= 1 + zoom_speed*(k['zoom in'] - k['zoom out'])
            translate = [t + q*this.shift_speed for q, t in zip((k['left'] - k['right'], k['up'] - k['down']), translate)]
            print(round(scaling, 3), translate)
            this.draw_options.transform = pymunk.Transform().translated(300, 300).scaled(scaling).translated(*translate).translated(-300, - 300)

    def camera_to_player(this):
        
        camera()

    def on_pause(this): 
        this.self.window_caption['pause'] = '(pause)'
        
    
    def input_controller(this):
        self = this.self
        for key, function in this.keymap:
            if self.key[key]: 
                function()
        

class lv_1(_level_):
    def __init__(this, self):
        super().__init__(self)
        
    def __call__(this, *args, **kwds):
        return super().__call__(*args, **kwds)
        
    def on_enter(this):
        super().on_enter()
        this