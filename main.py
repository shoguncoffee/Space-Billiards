import pygame, sys
from pygame.locals import *
import random
import tqdm
from Matter import *
from GUI import *
from OBJECT import *


class Game:

    def __init__(self):
        
        self.screen = pygame.display.set_mode(
            (600, 600),
            0,
            32
            )
        self.timer = pygame.time.Clock()
        
        player = self.character()
            
    
    def display(self):
        s = self.screen
        s.fill()
        s.blit(9,9)
        
    
    def run(self):
        pygame.init() 
        pygame.display.set_caption('game')
        while 1:
            self.display()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                    
            pygame.display.update()
            self.timer.tick(60)
    
    
if __name__ == '__main__':
    Game.run()
    