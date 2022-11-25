from __future__ import annotations
from .field import *
from .field import _field
        
        
class Show(_field):
    step_hz: int = 5
    blueprint = {'sand':{}}
    alias = {}
    
    def layer_mod(this):
        return {
            'gui': {
                'title':
                    this.text['subtitle'](
                        'Press [ SPACE BAR ] to Continue',
                        this.center[0], 480,
                        local = 'center'
                    ),
                'name': 
                    this.text['subtitle'](
                        '65010310 NATTAPON SUPAPHON',
                        994, 30,
                        local = 'topright',
                        color = (57, 57, 57, 60)
                    )
            }
        }
        
    def enter(this, **kw):
        if super().enter(**kw):
            this.fade = True
            this.tick = this.self.tick
            border = Borderline(
                (0, 0),
                (window_size[0], 0),
                (*window_size,),
                (0, window_size[1]),
                (0, 0),
                radius = 1
            )
            this.matter['border'] = [border]
            this.space.add(*border.object())
            for n in 'mac', 'nike', '3m', 'shell', 'samsung':
                x = random.randint(100, 900)
                y = random.randint(160, 480)
                r = lambda: random.randint(10000, 20000)
                this.add_matter(n, (x, y), local='center').body.apply_impulse_at_local_point((r(), r()))

        
    def general_func(this):
        this.simulate_func()
        
        if this.object['gui']['title'].fade(
            1.5, 
            25 if this.fade else 80
        ):
            if this.fade or this.self.tick - this.tick > 42:
                this.tick = this.self.tick
                this.fade = not this.fade

        if this.newpress(' '):
            this.goto('Normal', cache=False)



class Normal(_field):
    blueprint = {
        'player': {
        },
        'dick': {
        },
        'dude': {
        },
        'hole': {
        },
        'table': {
        },
        # 'man2': {
        #     'clone': 'dude' ,
        # },
    }
    alias = {
        'billiard': ('player', 'dick', 'dude')
    }
    
    def layer_mod(this):
        return {
            'background': {
                'guide': None,
                'hole': []
            },
            'gui': {
                'score':
                    this.text['title-heavy'](
                        '0', 900, 60,
                        local = 'midright',
                        color = (255, 255, 255),
                    ),
                'pull_point': 
                    None,
            }
        }
    
    
    def add_hole(this):
        topoffset = 64
        holelist = this.object['background']['hole']
        circle = this.self.preloaded['Circle']

        for x, y in product(*[
                (0, size - n) for size, n in zip(window_size, (0, topoffset))
            ]):
            c = lambda offset: (abs(x-offset), abs(y-offset) + topoffset)
            holelist.append(
                circle['bighole'](position=c(22))
            ) 
            this.add_matter('hole', c(31))

        for y in topoffset, -window_size[1]:
            x = this.center[0]
            holelist.append(
                circle['smallhole'](position=(x, abs(y + 14)))
            )
            this.add_matter('hole', (x, abs(y + 27)))

        
    def add_ball(this):
        seq = random.sample(
            ['dick', 'dude'], 
            counts = [6, 9], 
            k = 15
        )
        v = vector.unit().rotated_degrees(-60) * (2*10 + 1)
        start = vector(690, this.center[1] + 32)
        
        for i in range(5):
            for n in range(i+1):
                this.add_matter(
                    seq.pop(0), 
                    start - (0, 2 * n * v.y)
                )
            start += v
        
        
    def enter(this, **kw):
        if super().enter(**kw):
            
            this.score = 0
            this.pull_point: vector = vector.zero()
            this.click_working = True
            this.space.sleep_time_threshold = 20
            
            this.add_hole()
            this.table = this.add_matter('table')
            this.add_ball()
            this.player = this.add_matter('player', (240, this.center[1] + 32))
            
        else:
            this._response = this.last_response  
    
    
    def general_func(this):
        super().general_func()
        self = this.self
        click, clickchange = self.mousepress()
        this.player.first = True
        
        impulse = this.pull_point - this.mouse()
        if impulse.length > 250:
            impulse = impulse.scale_to_length(250)
        impulse *= 140
        
        
        if click and this.click_working:
            this.guide(impulse)
            if clickchange:
                this.pull_point = this.mouse()
                this.object['gui']['pull_point'] = self.preloaded['Circle']['guide'](
                    position = this.pull_point
                )
            if this.newpress(K_ESCAPE):
                this.click_working = False

        else:
            this.object['background']['guide'] = None
            this.object['gui']['pull_point'] = None
            if clickchange:
                if this.click_working:
                    this.player.body.apply_impulse_at_local_point(impulse)
                    this.simulate()
                    
                this.click_working = True
                
            if this.newpress(K_ESCAPE):
                this.goto('Main')
                
                
        if this.newpress(' '):
            if this.score >= 20:
                this.score -= 20
                this.object['gui']['score'] = this.text['title-heavy'](
                    str(this.score), 900, 60,
                    local = 'midright',
                    color = (255, 255, 255)
                )
                name = random.choices(['dude', 'dick'], [6, 4], k=1)
                x = random.randint(80, 950)
                y = random.randint(140, 500)
                this.add_matter(name[0], (x, y))
    
    
    
    def guide(this, impulse: vector):
        future = pymunk.Space()
        for body in this.space.bodies:
            clone = copy(body)
            future.add(clone)
            for s in body.shapes:
                shape = copy(s)
                shape.body = clone
                future.add(shape)
            
            if body is this.player.body:
                guide = clone
                
        guide.apply_impulse_at_local_point(impulse) # type: ignore
        this.object['background']['guide'] = []
        for _ in range(7):
            for _ in range(30): 
                future.step(this.step_dt)
            this.object['background']['guide'].extend([
                Circle(
                    1, 
                    color = (57, 57, 57),  # type: ignore
                    position = body.position, 
                    local = 'center'
                ) for body in future.bodies
            ])
            
            
    def sleep(this):
        stop = True
        remove: list[Matter] = []
        
        for matter in all_neat_value(this.matter):
            body: pymunk.Body = matter.body
            
            if hasattr(body, 'fall'):
                remove.append(matter)
                stop = False
            
            elif matter.body_type == pymunk.Body.DYNAMIC and not body.is_sleeping:
                v = body.velocity.length
                if v < .0009:
                    if not body.touch:
                        body.sleep() # type: ignore
                elif v > .006:
                    stop = False

        return stop, remove
        

    #this.simulate_fade() idea
    def simulate_func(this):
        super().simulate_func()
        
        stop, remove = this.sleep()
        for matter in remove:
            if matter.fade(1.5, 0):
                this.space.remove(*matter.body.constraints)
                this.remove_matter(matter)
                if matter is this.player:
                    this.goto(
                        'Done', 
                        cache = False, 
                        score = this.score if this.score >= 0 else 0
                    )
                    
                elif hasattr(matter.body, 'num'):
                    n = matter.body.num
                        
                    if matter.tag == 'dude':
                        this.score += round(
                            mountain_function(n, 30, 50, 10)
                        )
                    else:
                        this.score += round(
                            mountain_function(n, -10, 70, -50)
                        )
                    print(this.score)
                    this.object['gui']['score'] = this.text['title-heavy'](
                        str(this.score), 900, 60,
                        local = 'midright',
                        color = (255, 255, 255)
                    )
                    
                if len(this.matter['dude']) == 0:
                    this.goto('Done', cache=False, score=this.score)
                    
        if stop:
            this.to_general()
        
        if this.newpress(K_ESCAPE):
            this.goto('Main')
            
    
    
    @motion('billiard')
    def velocity_func(this, data: dict[str, Any]):
        body: pymunk.Body = data['body']
        if hasattr(body, 'fall'):
            data['damping'] = .999
            
        elif not body.is_sleeping and body.velocity.length > 1:
            data['gravity'] = this.get_gravity(
                body, *this.matter['hole']
            )
            
    @motion('player')
    def velocity_func(this, data: dict[str, Any]):
        body: pymunk.Body = data['body']
        v = body.velocity.length
        if hasattr(body, 'fall'):
            data['damping'] = .999
            
        elif not body.is_sleeping and v > 2:
            data['gravity'] = .3 * this.get_gravity(
                body, *this.matter['hole']
            )
        if this.player.first and v > 2:
            data['gravity'] += 50 * this.get_gravity(
                body, *this.matter['dude']
            )

    @touch()
    def begin(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        for shape in arbiter.shapes:
            shape.body.touch = True
        return True
    
    @touch()
    def separate(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        for shape in arbiter.shapes:
            shape.body.touch = False

    
    @touch('billiard')
    def separate(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        ball = arbiter.shapes[0].body
        if hasattr(ball, 'num'):
            ball.num += 1
        else:
            ball.num = 1
    
    
    @touch('billiard', 'billiard')
    def post_solve(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        sound = pygame.mixer.Sound('sound/1.mp3')
        sound.set_volume(arbiter.total_impulse.length/30_000)
        sound.play()
        
    @touch('billiard', 'table')
    def post_solve(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        sound = pygame.mixer.Sound('sound/table.mp3')
        sound.set_volume(arbiter.total_impulse.length/32_000)
        sound.play()
    
    
    @touch('player', 'billiard')
    def begin(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        this.player.first = False
        return True
    
    
    @touch('hole', 'billiard')
    def begin(this, arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        hole, ball = [shape.body for shape in arbiter.shapes]
        ball.fall = True
        table = this.table.body
        spring = pymunk.constraints.DampedSpring(
            table, ball,
            table.world_to_local(hole.position), (0, 0),
            0, 4700, 2400
        )
        space.add(spring)
        this.self.fall.play()
        return True