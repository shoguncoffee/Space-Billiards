from __future__ import annotations
from base import *
from pygame import gfxdraw
import pymunk.autogeometry as geometry

# what if each object own layer themself?

class Graphic:
    folder = 'img/'

    def __init__(self, 
            filename: str = '<runtime-local>', 
            tag: str = __qualname__, 
            position: coordinate = (0, 0), 
            local: str = 'topleft',
            online: bool = True,
            scale: int = 1,
            opacity: int = 100,
            **kw
        ):
        self.time_create = nowtime()
        self.filename = self.folder + filename
        self.tag = tag
        self.online = online
        self.local = local
        self.position = position
        
        self.render = self.load()
        self.scale = scale
        self.opacity = opacity
    
    
    def __call__(self, **kw):
        clone = copy(self)
        set_attr(clone, time_create=nowtime(), **kw)
        clone.render = self.render.copy()
        return clone
    
    
    def __repr__(self):
        l = super().__repr__().split(' ')
        l[1] = f'"{self.tag}" {self.time_create} topleft{self.rect.topleft}'
        adrss = int(l[3].removesuffix('>'), 16)
        base36 = numpy.base_repr(adrss, 36)
        l[3] = f"{base36.lower()}>"
        return ' '.join(l)
    
      
    # def __add__(self): idea Surface1 + Surface2 = Surface3.blits((Surface1, ...), ...)
    
      
    def load(self):
        if self.filename is None:
            return pygame.Surface((0, 0))
        
        return pygame.image.load(self.filename).convert_alpha()
    
    
    def enable(self):
        self.online = True
        
    def disable(self):
        self.online = False
        
    def set_invisable(self):
        self.opacity = 0
    
    def fade(self, speed: float = 100, opacity: int = 100):
        """without argument -> set opacity to 0"""
        
        now = self.opacity
        if (diff := opacity - now) == 0:
            return True
        
        self.opacity = now + speed*sign(diff) if abs(diff) > speed else opacity 
    
    # def move(self, x: float, y: float):
    #     self.original_position \
    #         = tuple(round(a) for a in (x, y))
    
    # def move_shift(self, x: float, y: float):
    #     self.original_position \
    #         = tuple(a + round(b) for a, b in zip(self.original_position, (x, y)))
    
    
    @property
    def local(self):
        return self._local
    
    @local.setter
    def local(self, local: str):
        if hasattr(self, '_local'):
            self.rect = self.rect.copy()
            setattr(self.rect, local, self.position)
        else:
            self.rect = pygame.Rect(0, 0, 0, 0)
            
        self._local = local 
    
    @property
    def for_blit(self):
        return self.render, self.rect
    
    @property
    def size(self):
        return self.rect.size
    
    @property
    def position(self) -> tuple[int, int]:
        return getattr(self.rect, self.local)
    
    @position.setter
    def position(self, position: coordinate):
        assert len(position) == 2
        c = tuple(round(_) for _ in position)
        
        self.rect = self.rect.copy()
        setattr(self.rect, self.local, c)
    
    @property
    def render(self):
        return self._render
    
    @render.setter
    def render(self, render: pygame.Surface):
        self._render = render
        self.rect = render.get_rect(**{self.local: self.position})
    
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, scale: int):
        self._scale = scale
        if scale != 1:
            self.render = pygame.transform.scale_by(self.render, scale)
    
    @property
    def opacity(self):
        alpha = self.render.get_alpha()
        if alpha is None:
            return 100
        return to_opacity(alpha)
    
    @opacity.setter
    def opacity(self, opacity: float):
        alpha = to_alpha(opacity)
        self.render.set_alpha(alpha)


class Matter(Graphic):
    non_update: set[str] = set()
    slow_friction: float = .25

    def __init__(self, 
            antialias: bool = False,
            curve: bool = False,
            tolerance: float = .5,
            body_type = pymunk.Body.DYNAMIC, # 0 = dynamic, 1 = kinematic, 2 = static
            world_friction: float = .82,
            friction: float = .01, 
            elasticity: float = .99, 
            density: float = 1,
            collision_type: int = 0, 
            group: int = 0,
            category: int = pymunk.ShapeFilter.ALL_CATEGORIES(),
            category_mask: int = pymunk.ShapeFilter.ALL_MASKS(),
            sensor: bool = False,
            **kw
        ):
        super().__init__(**kw)
        self.center = self.rect.center
        set_attr(self, **locals())
        self.set_physical()
        
        
    def __call__(self, **kw):
        clone = super().__call__(**kw)
        clone.body = self.body.copy()
        clone.shape_group = [shape.copy() for shape in self.shape_group]
        clone.update_physical()
            
        return clone
    
    
    def march(self):
        simplify = geometry.simplify_curves if self.curve else geometry.simplify_vertexes # type: ignore
        curvefit = geometry.march_soft if self.antialias else geometry.march_hard # type: ignore
        alphamap = pygame.surfarray.pixels_alpha(self.render)
        
        lineloops = curvefit(
            pymunk.BB(0, 0, *(q-1 for q in self.size)), 
            *self.size, 
            threshold = 128, 
            sample_func = lambda point: alphamap[int(point[0])][int(point[1])],
        )
        simplifyloop = [
            [v + (.5, .5) for v in simplify(line, self.tolerance)] # type: ignore
            for line in lineloops
        ]
        return simplifyloop
    
    
    def set_physical(self): 
        lineloops = self.march()
        convex_group = geometry.convex_decomposition(list(chain.from_iterable(lineloops)), 0)
        
        self.shape_group = [
            pymunk.Poly(None, convex, radius=.25) for convex in convex_group
        ]
        self.body = pymunk.Body(body_type=self.body_type) # type: ignore
        self.update_physical()
    

    def update_physical(self):
        self.filter = pymunk.ShapeFilter(self.group, self.category, self.category_mask) # type: ignore
        self.body.position = vector(*self.position)
        self.body.touch = False
        
        if hasattr(self, 'velocity_func'):
            self.body.velocity_func = self.velocity_func # type: ignore
        
        for shape in self.shape_group:
            copy_attr(self, shape, 
                *{
                    'body', 
                    'density', 
                    'friction', 
                    'elasticity', 
                    'filter', 
                    'collision_type', 
                    'sensor'
                } - self.non_update
            )
    

    def friction_func(self, body: pymunk.Body, dt: float):
        v = body.velocity
        u = v.length
        friction = self.world_friction if u > 3 else self.slow_friction # type: ignore
        F: float = friction * body.mass
        if u > .0001:
            body.apply_force_at_local_point(
                -v.scale_to_length(F), 
                body.center_of_gravity
            )
        pymunk.Body.update_position(body, dt)
    
        
    @property
    def for_blit(self):
        angle: float = self.body.angle
        img = pygame.transform.rotozoom(self.render, -math.degrees(angle), 1)
        local_center = -vector(*self.center)
        rotated_center = local_center.rotated(angle)
        world_rotated_center = [
            p-c for p, c in zip(self.body.position, rotated_center)
        ]
        return img, img.get_rect(center=world_rotated_center)
    
    
    def object(self):
        return self.body, *self.shape_group


class Shape(Graphic):                                
    def __init__(self, 
            color: color_type = (8, 8, 8), 
            **kw
        ):
        self.color = (*color, 255) if len(color) == 3 else color
        super().__init__(**kw)
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color: color_type):
        assert len(color) in (3, 4)
        self._color = (*color, self.color[3]) if len(color) == 3 else color
        
        if hasattr(self, 'render'):
            self.render = self.load()
        
    def color_alpha(self, alpha: int):
        return *self.color[:3], alpha
    
    def blit(self, 
            s: pygame.Surface, 
            r: pygame.Rect | tuple[int, int]
        ):
        self.render.blit(s, r, special_flags=pygame.BLEND_ALPHA_SDL2)
            
 
class Text(Shape):
    folder = 'font/'
    
    def __init__(self, 
            filename: str,
            font_size: int, 
            text: str = '', 
            antialias: bool = True, 
            **kw
        ):
        self._text = text
        self.antialias = antialias
        self.font = pygame.font.Font(self.folder + filename, font_size)
        super().__init__(filename=filename, **kw)
        
        
    def __call__(self, text: str = '', x: int = 0, y: int = 0, **kw):
        clone = super().__call__(position=(x, y), **kw)
        if text: 
            clone.text = text
        
        return clone
    
    @property
    def text(self):
        return self._text
        
    @text.setter
    def text(self, text):
        self._text = text
        self.render = self.load()
    
    def load(self):
        return self.font.render(self.text, self.antialias, self.color)
          

class Boundary(Matter):
    def __init__(self, 
            radius: int = 2,
            level: int = 0,
            **kw
        ):
        self.radius = radius
        self.level = level
        super().__init__(**kw)
    
    def set_physical(self):
        lineloops = self.march()
        assert len(lineloops) == 1, f'{self.tag} -> {len(lineloops)}\n{lineloops}'
        paths = lineloops[0]
        
        self.shape_group = [
            pymunk.Segment(None, start, end, radius=self.radius)
            for start, end in zip(paths, paths[1:])
        ]
        self.body = pymunk.Body(body_type=self.body_type) # type: ignore
        self.update_physical()
    

class Circle(Shape):
    offset = 2
    
    def __init__(self, 
            radius: int,
            width: int = 0,
            **kw
        ):
        self.radius = radius
        self.width = width
        super().__init__(**kw)
    
    def load(self):
        radius = self.radius
        width = self.width
        mid = radius + self.offset
        render = pygame.Surface(
            [mid*2 for _ in range(2)],
            pygame.SRCALPHA
        )
        render.fill(self.color_alpha(0))
        gfxdraw.aacircle(render, mid, mid, radius + 1, self.color_alpha(60))
        gfxdraw.aacircle(render, mid, mid, radius, self.color)
        gfxdraw.filled_circle(render, mid, mid, radius, self.color)
        if self.width:
            gfxdraw.aacircle(render, mid, mid, radius - width, self.color_alpha(0))
            gfxdraw.filled_circle(render, mid, mid, radius - width, self.color_alpha(0))
            
        return render
    
    
class Ball(Circle, Matter):
    non_update = {'density'}
    
    def __init__(self, 
            friction = .5,
            elasticity = .8,
            **kw
        ):
        kw.update(
            **{k: v for k, v in locals().items() if v not in (self, kw)}
        )
        super().__init__(**kw)
    
    @property
    def for_blit(self):
        return self.render, self.render.get_rect(center=self.body.position)
    
    def set_physical(self):
        shape = pymunk.Circle(None, self.radius)
        self.body = pymunk.Body(
            shape.area * self.density, # type: ignore
            float('inf')
        )
        self.shape_group = [shape]
        self.update_physical()
        

class Solid(Shape):
    def load(self):
        render = pygame.Surface(window_size, pygame.SRCALPHA)
        render.fill(self.color)
        
        return render
     
     
class Rectangle(Shape):
    offset = 1
    
    def __init__(self, 
            width: int, 
            height: int, 
            radius: int = 0, 
            **kw
        ):
        assert 0 <= radius <= min(width, height)/2
        self.width = width
        self.height = height
        self.radius = radius
        super().__init__(**kw)
    
    def load(self):
        render = pygame.Surface(
            [q + 2*self.offset for q in (self.width, self.height)],
            pygame.SRCALPHA
        )
        render.fill(self.color_alpha(0))
        pygame.draw.rect(
            render, 
            self.color,
            (self.offset, self.offset, self.width, self.height),
            border_radius = self.radius
        ) 
        return render
   
    
# class Box(Rectangle, Matter):
#     ...
    
    
class Line(Shape):
    def __init__(self, 
            *paths: tuple[int, int], 
            radius: int = 2,
            **kw
        ):
        self.path = paths
        self.radius = radius
        super().__init__(**kw)
        
    def load(self):
        f = lambda i: max(self.path, key=lambda q: q[i])[i] \
            - min(self.path, key=lambda q: q[i])[i]
            
        render = pygame.Surface(
            (f(0), f(1)), 
            pygame.SRCALPHA
        )
        render.fill(self.color_alpha(0))
        pygame.draw.aalines(render, self.color, False, self.path)
        return render
    
    
class Borderline(Line, Matter):
    non_update = {'density'}
        
    def set_physical(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_group = [
            pymunk.Segment(None, start, end, radius=self.radius)
            for start, end in zip(self.path, self.path[1:])
        ]
        self.update_physical()
        print(self.shape_group)
    

# class Poly(Graphic):
#     ...
   
   
# class Polygon(Shape, Matter):
#     def __init__(self, 
#             shape: list[dict[str, Any]], 
#             **kw
#         ):
#         self.shape = shape
#         super().__init__(**kw)
    
#     def load(self):
#         render = pygame.Surface(self.size, pygame.SRCALPHA)
#         for guide in self.shape:
#             func = getattr(pygame.draw, guide.pop('func'))
#             func(render, **guide)

#         return render
    