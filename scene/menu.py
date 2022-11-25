from __future__ import annotations
from .scene import *
from .scene import _scene


class _menu(_scene):
    unselect_opacity: int = 25
    fade_speed: int = 10
    
    def __init__(this, self):
        super().__init__(self)
        this.title = this.text['title'] 
        this.gateto = lambda scene, cache=True, **kw: lambda: this.goto(scene, cache, **kw)
        this.goback = lambda: this.goto(self.last_scene, new=False)
        
        
    def entering(this):
        if all([
                q.fade(20) for q in this.object['gui']['component']
            ]):
            return True
        

    def leaving(this):
        c = [v for k, v in this.object['gui'].items() if k in ('select', 'component')]
        if all([
                q.fade(25, 0) for q in all_neat_value(c)
            ]):
            return True
            
#________________________________________________________________________

class Main(_menu):    
    def layer_mod(this):
        return {
            'gui': {
                'component': do(
                    Solid(
                        color = (8, 8, 8, 120),
                    ),
                    Rectangle(
                        290, 290, 25,
                        position = this.center, 
                        color = (235, 235, 235, 230), 
                        local = 'center'
                    ),
                    func = 'set_invisable'),
                
                'select': this.new_selection({
                    this.gateto('Normal', cache=False): 
                        this.title(
                            'Regame', 
                            this.center[0], 218, 
                            local = 'center'
                        ),
                    this.gateto('Scoreboard'): 
                        this.title(
                            'Scoreboard', 
                            this.center[0], 288, 
                            local = 'center'
                        ),
                    this.gateto('Exit'): 
                        this.title(
                            'Exit', 
                            this.center[0], 358, 
                            local = 'center'
                        ),
                })
            }
        }

        
    def general_func(this):
        for n, title in enumerate(this.selected.list):
            this.selection_effect(n, title)
            if title.rect.collidepoint(*this.mouse()):
                this.selected(n)
                if this.click():
                    this.selected.pick()
        
        if this.newpress('s'):
            this.selected.next()
            
        if this.newpress('w'):
            this.selected.previous()
            
        if this.newpress(' '):
            this.selected.pick()
            
        if this.newpress(K_ESCAPE):
            this.goto('Normal', cache=False, new=False)
            
    def selection_effect(this, n: int, title: Graphic):
        title.fade(
            this.fade_speed, 
            100 if n == this.selected.index else this.unselect_opacity
        )
            

class Exit(_menu):
    def layer_mod(this):
        return {
            'gui': {
                'component': [
                    Solid(),
                    this.text['title'](
                        'Your progress will not be saved', 
                        *this.center,
                        local = 'center',
                        color = (255, 255, 255)
                    ),
                ],
                'title': 
                    this.text['subtitle'](
                        'Press [ SPACE BAR ] to Exit', 
                        this.center[0], 480,
                        local = 'center',
                        color = (255, 255, 255),
                        opacity = 70
                ),
            }
        }
    def enter(this, **kw):
        if super().enter(**kw):
            this.fade = True
            this.tick = this.self.tick
            
            
    def general_func(this):        
        if this.newpress(K_ESCAPE):
            this.goback()
            
        if this.newpress(' '):
            raise Exitgame
        
        if this.object['gui']['title'].fade(
            1.5, 
            25 if this.fade else 80
        ):
            if this.fade or this.self.tick - this.tick > 42:
                this.tick = this.self.tick
                this.fade = not this.fade

        
class Scoreboard(_menu):
    def layer_mod(this):
        data = list(json_to_items('score.json'))
        return {
            'gui': {
                'component': [
                    Solid(),
                    this.text['title-heavy'](
                        'Top 5',
                        this.center[0], 90,
                        local = 'center',
                        color = (255, 255, 255)
                    )
                ],
                'name': [
                    this.text['body'](
                        name, 
                        230, 115 + n*60,
                        color = (255, 255, 255),
                        local = 'topleft'
                    )
                    for n, (name, _) in enumerate(data[:5], 1)
                ],
                'score': [
                    this.text['body'](
                        f'{score}',
                        760, 115 + n*60,
                        color = (255, 255, 255),
                        local = 'topright'
                    )
                    for n, (_, score) in enumerate(data[:5], 1)
                ],
                'colon': [
                    this.text['body'](
                        ':',
                        600, 115 + n*60,
                        color = (255, 255, 255),
                        local = 'topleft'
                    )
                    for n, (_, _) in enumerate(data[:5], 1)
                ]
            }
        }
    
    def general_func(this):
        if this.newpress(K_ESCAPE):
            this.goback()
            
            
class Done(_menu):    
    def layer_mod(this):
        return {
            'gui': {
                'component': [
                    Solid(),
                    this.text['title-heavy'](
                        'Your Score',
                        this.center[0], 100,
                        local = 'center',
                        color = (255, 255, 255)
                    ),
                    this.text['title'](
                        f'{this.score}',
                        this.center[0], 160,
                        local = 'center',
                        color = (255, 255, 255)
                    )
                ],
                'input': 
                    None,
                    
                'title': 
                    this.text['subtitle'](
                        'Press [ ENTER ] to save', 
                        this.center[0], 480,
                        local = 'center',
                        color = (255, 255, 255),
                        opacity = 70
                ),
            }
        }

    def enter(this, score: int| None = None, **kw):
        if score is not None: 
            this.score = score
            
        this.input = ''
        super().enter(**kw)
        this.fade = True
        this.tick = this.self.tick
        
        
    def general_func(this):
        for n, _ in enumerate(this.self.key):
            if this.newpress(n) and len(this.input) < 30:
                key = pygame.key.name(n)
                if len(key) == 1:
                    if this.press(K_RSHIFT) or this.press(K_LSHIFT):
                        this.input += key.upper()
                    else:
                        this.input += key
                        
                elif n == K_SPACE:
                    this.input += ' '
        
        this.object['gui']['input'] = this.text['body'](
            this.input,
            *this.center,
            local = 'center',
            color = (255, 255, 255),
        )
                    
        if this.newpress(K_BACKSPACE):
            this.input = this.input[:-1]
           
        if this.newpress(K_KP_ENTER) or this.newpress(K_RETURN):
            data = dict(json_to_items('score.json'))
            
            if this.input in data and data[this.input] > this.score:
                ...
                
            else:
                data[this.input] = this.score
                data = dict(
                    sorted(
                        data.items(), 
                        key = lambda t: t[1], 
                        reverse = True
                    )
                )
                with open('score.json', 'w') as f:
                    f.write(
                        json.dumps(data, indent=4)
                    )
                
            this.goto('Show', cache=False)
            
        if this.newpress(K_ESCAPE):
            this.goto('Show', cache=False)
            
            
        if this.object['gui']['title'].fade(
            1.5, 
            25 if this.fade else 80
        ):
            if this.fade or this.self.tick - this.tick > 42:
                this.tick = this.self.tick
                this.fade = not this.fade