from base import *

#from scene import * 
#print(*[f'{q}\t{e}' for q, e in locals().items() if not q.startswith('_')], sep='\n')

# import scene.scene
# print(scene.scene._scene)

#foo = __import__('scene.scene')
#print(foo.scene._scene)


# mod = __import__(f'obj')
# from obj import __all__ as files
# print(files)

# modules = [__import__(f'obj.{f}').obj for f in files]
# print(mod)
# print(modules[0].Graphic)

    
# print(*cls_from_module(folder='obj'))


#q = obj.Text('asd')
#l = q('hello', 1, 2)
#print(obj)
# obj = {
#     'background': {
#         'cache': []
#     },
#     'matter': {
#         'Ball': [5],
#         'cache': ['xxx']
#     },
#     'gui': {
#         'title': [1,2,3],
#         'cache': []
#     },
#     'window': {
#         'fade': '123',
#         'pause': {
#             'component': [
#                 '555',
#             ],
#             'select': {
#             }
#         },
#         'exit': {
#             'component': [
#             ],
#             'select': {
#             }
#         },
#     }
# }

# def to_cache(cache):
#     d = {n: {'cache': v} for n, v in cache.items() if n != 'window'}
#     print('to', d)
#     return d

# def from_cache(cache):
#     d = {n: v['cache'] for n, v in cache.items() if n != 'window'}
#     print('from', d)
#     return d

# x = to_cache(obj)
# d = from_cache(x)
# c = to_cache(x)
# from_cache(c)


# class DummyContextManager(object):
#     def __enter__(self):
#         print('Entering...')
#     def __exit__(self, exc_type, exc_value, traceback):
#         print(exc_type, exc_value, traceback)  
#         if exc_type is Exitgame:
#             return True
#         # If we returned True here, any exception would be suppressed!

# with DummyContextManager():
#     raise Exitgame()

print(
    os.listdir(
        '\\'.join(__file__.split('\\')[:-1])
    )
    )