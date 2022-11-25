from __future__ import annotations
from base import *
from pygame.locals import *
from obj import *


class _selector: 
    def __init__(self, choice: choice_type):
        self._index = 0
        self.length = len(choice)
        self.command = tuple(choice)
        self.list = tuple(choice.values())
    
    def __call__(self, n: int):
        self.index = n
    
    @property
    def index(self):
        return self._index
        
    @index.setter
    def index(self, n):
        self._index = n % self.length
        
    def pick(self):
        print('pick')
        self.command[self.index]()
        
    def next(self):
        self.index += 1
    
    def previous(self):
        self.index -= 1
    

# รวบฟังชันเป็น class window เช่น class pause(window) กับ exit 
# ใช้กับ decorator?

# @window
# class pause:
#

class _scene:    
    def __init__(this, self: Game):
        this.self = self
        this.text: dict[str, Text] = self.preloaded['Text'] # type: ignore
        
        this.center = [_//2 for _ in window_size]
        this.mouse = lambda: vector(*pygame.mouse.get_pos())
        this.changeclick = lambda x=0: self.mousepress(x)[1]
        this.click = lambda x=0: self.mousepress(x)[0]
        
        this.newpress: Callable[[str | int], bool] \
            = lambda x: all(self.keypress(x))
            
        this.press: Callable[[str | int], bool] \
            = lambda x: self.keypress(x)[0]
        
        this.add_layer: Callable[[dict[str, Any]], None] \
            = lambda d: updater(this.object, d)


    def new_obj(this) -> object_type:
        return {
            'background': {
            },
            'matter': {
            },
            'gui': {
            }
        }
    
        
    def layer_mod(this) -> object_type:
        return {}
    
    
    def draw(this):
        for obj in all_neat_value(this.object):
            if obj is not None and obj.online:
                this.self.window.blit(
                    *obj.for_blit, 
                    special_flags=BLEND_ALPHA_SDL2
                )
                # _, rect = obj.for_blit
                # pygame.draw.circle(
                #     this.self.window, (0, 0, 255), rect.topleft, 1
                # )
                # pygame.draw.circle(
                #     this.self.window, (0, 0, 255), rect.center, 1
                # )
                # pygame.draw.circle(
                #     this.self.window, (0, 0, 255), rect.bottomright, 1
                # )

        
        
    def new_selection(this, choice: choice_type):
        this.selected = _selector(choice)
        for text in choice.values():
            text.opacity = 0
            
        return choice
        
    
    @property
    def response(this):
        return this._response
    
    @response.setter
    def response(this, func: Callable):
        this.last_response = this._response
        this._response = func
        print(f'change {this.last_response} -> {func}')
    
    
    def goto(this, scene: str, cache: bool = True, **kw):
        if cache:
            kw['raw_object'] = this.object

        this.leave(
            lambda: this.self.openscene(scene, **kw)
        )
    
    
    def to_general(this):
        this.response = this.general_func
    
    
    def enter(this, 
            new: bool = True, 
            raw_object: object_type = {},
        ):
        """return True if scene is recreate"""
        this._response = lambda: setattr(this, 
            'response', this.general_func
        ) if this.entering() else None
        
        if new:
            this.start_time = time()
            this.object = this.new_obj()
            this.add_layer(this.to_cache(raw_object))
            this.add_layer(this.layer_mod())
            return True
        
        
    def entering(this) -> bool:
        print('entering')
        return True
    
    
    def leave(this, after: Callable = lambda: None):
        this.response = lambda: after() if this.leaving() else None
        
    
    def leaving(this) -> bool:
        print('leaving')
        return True
    
    
    def general_func(this):
        ...

    
    def selection_effect(this, 
            n: int, 
            title: Graphic
        ):
        opacity = 100 if n == this.selected.index else 30
        title.fade(20, opacity)
        
        
    @staticmethod
    def to_cache(cache: object_type) -> object_type:
        return {
            n: {'cache': v} for n, v in cache.items()
        }
    
    @staticmethod
    def from_cache(cache: object_type) -> object_type:
        return {
            n: v['cache'] for n, v in cache.items()
        }