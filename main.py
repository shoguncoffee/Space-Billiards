import pygame, sys
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode(
    (600, 600),
    0,
    32
    )
pygame.display.set_caption('game') 

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
    pygame.display.update()
    
    
    