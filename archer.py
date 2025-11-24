from pico2d import load_image
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP
import game_world
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class RUN:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_run.png')

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
       self.archer.frame = (self.archer.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.archer.frame * 120 ,0, 120, 100, self.archer.x, self.archer.y)

class IDLE:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_idle.png')

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.archer.frame = (self.archer.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.archer.frame * 120, 0, 120, 100, self.archer.x, self.archer.y)


class ATTACK:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_attack.png')
        self.archer_arrow = 0

    def enter(self, e):
        self.archer.frame = 0
        self.archer_arrow = 0

    def exit(self, e):
        self.archer_arrow = 0

    def do(self):
        self.archer.frame = (self.archer.frame + 1) % 3
        self.archer_arrow += 1

        if self.skill_arrow == 3:
            self.archer.state_machine.cur_state = self.archer.archer_idle
            self.archer.archer_idle.enter(None)


    def draw(self):
        self.image.clip_draw(self.archer.frame * 120, 0, 120, 100, self.archer.x, self.archer.y)


class archer:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.hp = 180
        self.str = 45

        self.archer_idle = IDLE(self)
        self.archer_attack = ATTACK(self)
        self.archer_run = RUN(self)
        self.state_machine = StateMachine(
            self.archer_run,
            {
                self.archer_idle: {space_down: self.archer_attack},
                self.archer_attack: {space_down: self.archer_idle},
                self.archer_run : {}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def use_skill(self):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.archer_idle
        self.archer_idle.enter(None)


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
