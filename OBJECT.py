import pygame


class Matter:
    def __init__(self, file, coor, hp, mass, model):
        self.location = coor
        self.image = pygame.image.load(file)
        pass


class Character(Matter):
    def __init__(self, hp, mass, model, stemina, speed):
        
        super().__init__(hp, mass, model)
        
    
        
    pass