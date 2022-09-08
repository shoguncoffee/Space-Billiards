from base import *
from gui import *
from item import *
from myobject import *
from scene import *

class Exitgame(Exception):
    pass

class Game:
    window_size = 800, 800
    color_bit = 8
    window_caption = 'shogun game'
    max_fps = 60
    
    press_key = pygame.key.get_pressed()
    dataclass = Character, Weapon, Text

    @staticmethod
    def raise_exit():
        raise Exitgame
    
    def __init__(self):
        self.input_respone = {
            pygame.QUIT: self.raise_exit,
            pygame.WINDOWFOCUSLOST: lambda event: self.stop_game 
            }
        self.timer = pygame.time.Clock()
        self.data_initer()
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            depth=self.color_bit*4
            )
        pygame.display.set_caption(self.window_caption)
        
    def stop_game(self):
        pass
        if 
    
    def data_initer(self):
        for cls in self.dataclass:
            classname = cls.__name__
            data = json_to_dict(f'{classname}_attribute.json')
            info = {name: cls(**attr) for name, attr in data.items()}
            setattr(self, classname, info)
    
    def handle_input(self):
        for event in pygame.event.get():
            respone_func = self.input_respone.get(event.type, lambda k: None)
            respone_func(event)
    
    def run(self):
        try: 
            self.scene = sc_menu(self)
            while 1:
                self.handle_input()
                self.scene.run()
                pygame.display.update()
                self.timer.tick(self.max_fps)
        except Exception as e:
            log(e)
        finally:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    mygame = Game()
    mygame.run()
    