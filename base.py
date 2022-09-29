import pygame, sys
import random
import tqdm
import json
import pymunk
import pymunk.pygame_util as pymunk_to_pygame
from pymunk.vec2d import Vec2d as vector
from time import *
from typing import overload


class Exitgame(Exception):
    pass

def raiser(exception):
    raise exception

def json_to_dict(file):
    with open(file) as f:
        return json.load(f)

@overload
def log(*s, t=None, multiline=False, end='\n', sep=' ') -> None:
    dash = ' '*13 + '-'
    if t is None: 
        t = strftime("%X")
        a = ''
    elif t is False:
        t = ''
        a = dash
    if multiline: 
        sep = '\n' + dash
        
    print('%-7s'%t, a, sep.join(str(q) for q in s), end=end, sep='')
    
@overload
def log() -> None:
    print()
    
def repeat(func, n):
    for _ in range(n):
        func()