import pygame, sys
import random
import tqdm
import pymunk
import json
from time import *

def json_to_dict(file):
    with open(file) as f:
        return json.load(f)
    
def log(*s, t=None, multiline=False, end='\n', sep=' '):
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