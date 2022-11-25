from __future__ import annotations
from .scene import *
from .scene import _scene
from pymunk import pygame_util


class touch:
    cache: list[touch] = []
    
    def __init__(self, 
            a: None | str | list[str] = None, 
            b: None | str | list[str] = None
        ):
        self.pack = (q if isinstance(q, list) else [q] for q in (a, b))
    
    def __call__(self, 
            callback: Callable[
                [Any, pymunk.Arbiter, pymunk.Space, dict], None | bool
            ]
        ):
        self.when = callback.__name__
        assert self.when in ('begin', 'pre_solve', 'post_solve', 'separate')
        self.wraper = lambda this: lambda *arg, **kw: callback(this, *arg, **kw)
        type(self).cache.append(self)
    
    @classmethod
    def init(cls, attr):
        group: dict[str | None, tuple[str, ...]] = attr['alias']
        blueprint: object_type = attr['blueprint']
        
        for self in cls.cache:
            unpack = [
                [k for i in l for k in group.get(i) or (i,)] 
                for l in self.pack
            ]
            for pair in product(*unpack):
                pair_id = [
                    None if name is None else blueprint[name]['collision_type'] 
                    for name in pair
                ]
                # handle lambda in loop problem
                f = lambda instance, id: \
                    lambda this: instance.set(this, *id)
                yield f(self, pair_id)
                
        cls.cache = []

    def set(self, this: _field, a: int | None, b: int | None):
        space = this.space
        if a is None:
            handle = space.add_default_collision_handler()
        elif b is None:
            handle = space.add_wildcard_collision_handler(a)
        else:
            handle = space.add_collision_handler(a, b)
        
        setattr(handle, self.when, self.wraper(this))
    

class motion: 
    cache: list[motion] = []
    
    def __init__(self, *name: str): 
        self.tag = name
    
    def __call__(self, 
            callback: Callable[
                [Any, dict[str, Any]], None
            ]
        ):
        assert callback.__name__ == 'velocity_func'
        self.callback = callback
        self.wraper = lambda this: \
            lambda *arg, **kw: self.set(this, *arg, **kw)
        type(self).cache.append(self)

    @classmethod
    def init(cls, attr: dict[str, Any]):
        group = attr['alias']
        blueprint: object_type = attr['blueprint']
        for self in cls.cache: 
            for name in self.tag: 
                for n in group.get(name) or [name]:
                    # lambda in loop?
                    f = lambda instance, _name: \
                        lambda this: blueprint[_name].update(
                            velocity_func = instance.wraper(this)
                        )
                    yield f(self, n)
        
        cls.cache = []
    
    def set(self, 
            this: _field,
            body: pymunk.Body, 
            gravity: coordinate, 
            damping: float, 
            dt: float
        ):
        data = {q: v for q, v in locals().items() if v not in (self, this)}
        self.callback(this, data) # update/change "data"
        pymunk.Body.update_velocity(*data.values())


class __update_callback(type):
    def __new__(cls, 
            clsname: str, 
            base: tuple[type, ...], 
            attr: dict[str, Any]
        ):
        n = count(1)
        for mod in chain(attr['blueprint'].values()):
            mod['collision_type'] = next(n)
        
        attr['callback'] = {
            n: list(callback.init(attr))
            for n, callback in (
                ('collision', touch), 
                ('velocity', motion)
            )
        }
        return super().__new__(cls, clsname, base, attr)


class _field(_scene, metaclass=__update_callback):
    callback: dict[str, list[Callable[[_field], None]]]
    step_hz: int = 30
    G: float = .0042
    
    blueprint: object_type = {
        # 'black hole': {'category': int, ...} 
    }
    alias: dict[str, tuple[str, ...]] = {
        # 'star': ('sun', 'black hole') // "sun", "black hole" in preloaded is True
    }
    
    def __init__(this, self: Game):
        super().__init__(self)
        this.step_per_frame = 60 / self.max_fps * .135
        this.step_dt = this.step_per_frame / this.step_hz
        this.option = pygame_util.DrawOptions(self.window)


    def draw(this):
        super().draw()
        # this.space.debug_draw(this.option)
        
        
    def enter(this, **kw):
        if super().enter(**kw):
            this.matter: dict[str, list[Matter]] = this.object['matter']
            this.gui: dict[str, list[Graphic]] = this.object['gui']
            this.space = pymunk.Space()
            this.init_callback()
            return True

        
    # def entering(this):
    #     if this.object['window']['fade'].fade(20, 0):
    #         this.object['window']['fade'].disable()
    #         return True
        

    # def leave(this):
    #     super().leave()
    #     this.object['window']['fade'].enable()
        
        
    # def leaving(this):
    #     if this.object['']['fade'].fade(20, 100):
    #         return True
        
        
    def simulate(this):
        this.response = this.simulate_func
    
    
    def simulate_func(this):
        for _ in range(this.step_hz): 
            this.space.step(this.step_dt)
    
    
    def add_matter(this, 
            tag: str, 
            position: coordinate = (0, 0), 
            nickname: str = '', 
            **modifly
        ):
        allmatter = enumerate_dict(this.self.preloaded)
        if (custom := this.blueprint.get(tag)):
            modifly = custom | modifly
        
        instance = allmatter[modifly.get('clone') or tag]
        assert isinstance(instance, Matter), f'"{instance}" is not matter'
        copied = instance(**modifly, position=position)
        
        if copied.body.moment == float('inf'):
            copied.body.position_func = copied.friction_func
        
        this.matter.setdefault(nickname or tag, []).append(copied)
        this.space.add(*copied.object())
        return copied

    
    def remove_matter(this, instance: Matter, label: str = ''):
        this.space.remove(*instance.object())
        if label:
            this.matter[label].remove(instance)
        else:
            for i in this.matter.values():
                if instance in i:
                    i.remove(instance)
                    break
            else:
                raise ValueError(f'{instance} not in list')
        
    
    def clear_matter(this, label: str):
        for matter in this.matter[label]:
            this.space.remove(*matter.object())
            
        this.matter[label] = []
    

    def get_gravity(this, passive: pymunk.Body, *active: Matter):
        point = passive.position
        field = vector.zero()
        for matter in active:
            body = matter.body
            field += this.gravity_field(point, body.position, body.mass)
        
        return this.G * passive.mass * field
    
    
    @staticmethod
    def gravity_field(passive: vector, active: vector, Mass: float):
        direction =  active - passive
        try:
            factor = Mass/passive.get_dist_sqrd(active)
        except ZeroDivisionError:
            return vector.zero()
        
        return direction.scale_to_length(factor)
    
    
    def velocity_func(this, data: dict[str, Any]): ... # modify/update dict
    def begin(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict) -> bool: return True
    def pre_solve(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict) -> bool: return True
    def post_solve(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict): ...
    def separate(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict): ...
    def init_callback(this):
        for callback in chain.from_iterable(this.callback.values()):
            callback(this)
            
        print(this.space._handlers.keys())