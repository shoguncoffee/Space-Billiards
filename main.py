from __future__ import annotations
from base import *


class Game:
    max_fps = 60

    def __init__(self):
        self.start_time = nowtime()
        pygame.init()
        random.seed()
        self.timer = pygame.time.Clock()
        self.ticker = cycle(range(18_000))
        self.tick = next(self.ticker)
        self.input_response = {
            pygame.QUIT: lambda: self.current_scene.goto('Exit'),
            # pygame.WINDOWCLOSE: lambda: self.current_scene.pause(),
        }
        self.window = pygame.display.set_mode(
            window_size,
            pygame.SRCALPHA,
            vsync = 1,
        )
        self.preloading()
        self.init_scene()
        try:
            pygame.mixer.music.load('sound/pool.mp3')
            pygame.mixer.music.set_volume(.15)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass  # background music is not included in the repository
    
    
    def preloading(self):
        import obj
        class_pack = {cls.__name__: cls for cls in cls_from_module(obj)}
        self.preloaded: dict[str, dict[str, obj_type]] = {}
        
        for clsname, instance_group in json_to_items('Attribute.json'):
            cls = class_pack[clsname]
            self.preloaded[clsname] = {}
            for objname, attr in instance_group.items():
                instance = cls(**attr, tag=objname)
                self.preloaded[clsname][objname] = instance

        path = __file__.split('\\')
        path[-1] = 'sound'
        path = '\\'.join(path)
        self.fall = pygame.mixer.Sound(r'sound\fall.mp3')
        self.fall.set_volume(.8)
    
    def init_scene(self):
        self.scene: dict[str, scene_type] = {
            cls.__name__: cls(self) for cls in cls_from_module(folder='scene')
        }
        self.openscene('Show')
    
    
    def openscene(self, scene: str, **kw):
        try: self.last_scene = self.current_scene.__class__.__name__
        except: ...
        self.current_scene = self.scene[scene]
        self.current_scene.enter(**kw)
    
    @property
    def key(self):
        return self._key
    
    @property
    def mouse(self): # [left, center, right]
        return self._mouse
    
    @key.setter
    def key(self, key):
        try: self._cachekey = self.key
        except: self._cachekey = key
        self._key = key
    
    @mouse.setter
    def mouse(self, mouse):
        try: self._cachemouse = self.mouse
        except: self._cachemouse = mouse
        self._mouse = mouse
        
    def mousepress(self, c: int = 0):
        new = self.mouse[c]
        cache = self._cachemouse[c]
        change = cache != new
        return new, change
    
    def keypress(self, c: str | int):
        key_code = pygame.key.key_code(c) if isinstance(c, str) else c
        new = self.key[key_code]
        cache = self._cachekey[key_code]
        change = cache != new
        return new, change
    
    def handle_input(self):
        self.key = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            self.input_response.get(event.type, lambda: None)()
    
        
    def draw(self):
        self.buffer = self.window.copy()
        self.buffer.set_alpha(85)
        
        self.window.fill(C_background)
        self.window.blit(self.buffer, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        self.current_scene.draw()
        pygame.display.set_caption(
            f'Space Billiard {round(self.timer.get_fps())}'
        )
        pygame.display.update()
    
    
    def run(self):
        while 1: 
            self.tick = next(self.ticker)
            self.handle_input()
            self.current_scene.response()
            self.draw()
            self.timer.tick(self.max_fps)
    
    
    def __enter__(self):
        return self
            
    def __exit__(self, type, value, traceback):
        if type is Exitgame:
            pygame.quit()
            return True


if __name__ == '__main__':
    with Game() as mygame:
        mygame.run()