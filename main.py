from base import *
from gui import *
from item import *
from myobject import *
from scene import *

class Game:
    window_size = 800, 800
    color_bit = 8
    window_caption = 'shogun game'
    fps = 60
    
    press_key = {pygame.key.name(i): 0 for i in range(128)}
    dataclass = [Character, Weapon]

    def data_initer(self):
        for cls in self.dataclass:
            classname = cls.__name__
            data = json_to_dict(f'{classname}_attribute.json')
            info = {name: cls(**attr) for name, attr in data.items()}
            setattr(self, classname, info)
    
    def __init__(self):
        self.input_respone = {
            pygame.QUIT: lambda k: (pygame.quit(), sys.exit()),
            pygame.KEYDOWN: lambda k: self.press_key.update({pygame.key.name(k['key']): True}),
            pygame.KEYUP: lambda k: self.press_key.update({pygame.key.name(k['key']): False}),
            }
        
        self.timer = pygame.time.Clock()
        self.data_initer()
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            depth=self.color_bit*4
            )
        pygame.display.set_caption(self.window_caption)
              
    def handle_input(self):
        for event in pygame.event.get():
            respone_func = self.input_respone.get(event.type, lambda k: None)
            respone_func(event.__dict__)
    
    def run(self):
        self.sc_menu()
        while 1:
            self.handle_input()
            self.operate()
            pygame.display.update()
            self.timer.tick(self.fps)
            
    
if __name__ == '__main__':
    mygame = Game()
    mygame.run()
    