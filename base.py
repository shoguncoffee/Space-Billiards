from __future__ import annotations
import sys, warnings, os
import numpy, random, math
import pymunk, pymunk.pygame_util
import pygame
import tqdm
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
from typing import ItemsView, Any, Callable, Type, TYPE_CHECKING, Generator, TypeVar, Union, Sequence, Optional
from itertools import cycle, product, count, chain
from pymunk.vec2d import Vec2d as vector
from copy import copy
from time import *


C_background = 220, 222, 229
B_background = 63, 64, 65
window_size = 1024, 576

if TYPE_CHECKING:
    from obj import Graphic, Text, Matter, Shape
    from scene import scene, menu, play, field
    from main import Game
    
    iterable = dict | list | tuple
    obj_type = Graphic | Text | Matter
    scene_type = scene._scene | menu._menu | field._field
    coordinate = vector | tuple[float, float] | list[float]
    color_type = tuple[int, int, int] | tuple[int, int, int, int]
    object_type = dict[str, dict[str, Any]]
    choice_type = dict[Callable[[], None], Graphic]


class Exitgame(Exception):
    pass


def raiser(exception):
    raise exception


def json_to_items(file: str):
    with open(file) as f:
        d: dict[str, Any] = json.load(f)
    return d.items()


def log(*s, t=None, multiline=False, end='\n', sep=' '):
    dash = ' '*13 + '-'
    a = ''
    if t is None: 
        t = strftime("%X")
    elif t is False:
        t = ''
        a = dash
    if multiline: 
        sep = '\n' + dash
        
    print('%-7s'%t, a, sep.join(str(q) for q in s), end=end, sep='')
    
    
def repeat(n: int, func: Callable):
    for _ in range(n): func()
        

def cls_from_module(*modules, folder='') -> Generator[Type, None, None]:
    if folder:
        files = __import__(folder).__all__        
        modules = [getattr((__import__(f'{folder}.{f}')), f) for f in files]
        yield from cls_from_module(*modules)
        
    else:
        for module in modules:
            for obj in module.__dict__.values():
                if isinstance(obj, type) \
                        and obj.__module__ == module.__name__ \
                        and not obj.__name__.startswith('_'):
                    yield obj
           
                
def all_neat_value(obj: iterable): 
    iterater = (dict, list, tuple)
    assert obj not in iterater, f'Not iterable: {obj}'
    
    for q in (obj if not isinstance(obj, dict) else obj.values()):
        if isinstance(q, iterater):
            yield from all_neat_value(q)
        else: 
            yield q
        
            
def get_from_neat_dict(d: dict, key: Any): #!
    # all neat key shouldn't duplicate
    for k, v in d.items():
        if k == key:
            return v
        
        elif isinstance(v, dict):
            r = get_from_neat_dict(v, key)
            if r: return r
            
    raise KeyError


'''
def dict_insert(d: dict, dept: list[str], value):
    last = dept[-1]
    l = d
    for k in dept:
        p = l
        l = l.get(k)
        assert l is not None or k == last, f'{d}, {dept}'
        
    if k is None:
        p[last] = value
    else:
        p[last]
'''         
    
            
def updater(objmap: dict[str, Any], sample: dict[str, Any]):
    for key, val in sample.items():
        i = objmap.get(key)
        
        if i is None:
            objmap[key] = val
        
        elif isinstance(i, dict):
            assert isinstance(val, dict)
            updater(i, val)
              
        elif isinstance(i, list):
            if isinstance(val, list):
                i.extend(val)
            else:
                i.append(val)
        
        else:
            raise TypeError(
                f'{type(i)} not updatable \n >>> {objmap} \n >>> {sample}'
            )

  
def nowtime():
    return strftime('%X')
    
    
def mountain_function(input, peak=1, thickness=1, base=0):
    return (peak - base)/(input**2 /thickness + 1) + base


def anyin(d: dict, *sample):
    return any(q in d for q in sample)


def bin_on_digit(n):
    return 1 << n


def set_attr(
        obj: object, 
        include_None: bool = True,
        include_dict: bool = False, 
        include_dunder: bool = False,
        **kw
    ):
    for k, v in kw.items():
        if not any([
            v is obj,
            not include_dict and isinstance(v, dict),
            not include_None and v is None,
            not include_dunder and k.startswith('_')
        ]):
            setattr(obj, k, v)


def copy_attr(haveattr: object, wantattr: object, *attrname: str):
    for n in attrname:
        setattr(wantattr, n, getattr(haveattr, n))
        
        
def condition_path(*arg, call=False): # avoid long if else
    for b, f in zip(arg[::2], arg[1::2]):
        if b: 
            return f() if call else f    
        

def do(*q, func: str, **arg):
    for obj in all_neat_value(q):
        getattr(obj, func)(**arg)
            
    return q


def sign(n: float):
    return (n>0) - (n<0)


def merge_dict(*d: dict):
    new = {}
    for i in d:
        new.update(**i)
    return new


def enumerate_dict(d: dict[Any, dict]):
    new = {}
    for v in d.values():
        new.update(v)

    return new


def to_alpha(n: float):
    return round(n/100 * 255)
    
def to_opacity(n: float):
    return round(n/255 * 100)


if __name__ == '__main__':
    # l = cycle(range(3))
    # while 1:
    #     print(next(l))
    #     sleep(1)
    # print(*product([9,8,7], [1
    #                          ]))
    j = enumerate_dict({
        'head': {
            1: 11,
            2:3
        },
        'hand': {
            9: 99,
            4: 0
        }
    })
    print(j)