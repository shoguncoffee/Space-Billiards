import os

dir = os.listdir(__file__.removesuffix('__init__.py'))
file = [
    f.removesuffix('.py') for f in dir 
    if f.endswith('.py') and not f.startswith('_')
]
__all__ = file # type: ignore
# __all__ = ['play', 'field', 'menu', 'scene']

if __name__ == '__main__':
    print(__all__)