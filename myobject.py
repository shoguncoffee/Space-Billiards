import pymunk
from base import *

class Appearance:
    def __init__(self):
        pass
    
    def draw(self, surface):
        self.

class Interface(pygame.sprite.Sprite, Appearance):

    def __init__(self):
        super().__init__()
        
    def Botton(Interface):
        def __init__(self):
            super().__init__()
        
    def Text(Interface):
        def __init__(self) -> None:
            pass


class Matter(Appearance):
    def __init__(self, file, coor, hp, mass, model):
        super().__init__()
        self.location = coor
        self.image = pygame.image.load(file).convert_alpha()
        
        self.body = pymunk.Body()
        self.shape = pymunk.Circle
    
    def moving():
        pass

class Material(Matter):
    def __init__(self, hp, mass, model, stemina, speed):
        
        super().__init__(hp, mass, model)
        
    
        
    def die():
        pass 

class Character(Matter):
    def __init__(self, hp, mass, model, stemina, speed):
        
        super().__init__(hp, mass, model)
        
    
        
    def melee():
        pass

class Platform(Matter):
    def __init__(self, hp, mass, model, stemina, speed):
        super().__init__(hp, mass, model)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        
    def draw():
        pass
    
    