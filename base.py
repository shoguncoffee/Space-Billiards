import pygame, sys
import random
import tqdm
import pymunk
import json

def json_to_dict(file):
    with open(file) as f:
        return json.load(f)
    
def log()
    