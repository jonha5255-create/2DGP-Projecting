from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP
import game_world
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE



class RUN:
    def __init__(self, healer):
        self.healer = healer
        self.image = load_image('healer run.png')

    def enter(self,e):
        self.healer.frame = 0

    def exit(self,e):
        pass

    def do(self):
       self.healer.frame = (self.healer.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.healer.frame * 100 ,0, 100, 100, self.healer.x, self.healer.y)


class IDLE:
    def __init__(self,healer):
        self.healer = healer
        self.image = load_image('healer idle.png')

    def enter(self,e):
        self.healer.frame = 0

    def exit(self,e):
        pass

    def do(self):
       self.healer.frame = (self.healer.frame + 1) % 2

    def draw(self):
        self.image.clip_draw(self.healer.frame * 100 ,0, 100, 100, self.healer.x, self.healer.y)

class HEAL:
    def __init__(self, healer):
        self.healer = healer
        self.image = load_image('healer heal.png')
        self.skill_heal = 0

    def enter(self,e):
        self.healer.frame = 0
        # 힐 시전시 프레임
        self.skill_heal = 0

    def exit(self,e):
        self.skill_heal = 0

    def do(self):
        self.healer.frame = (self.healer.frame + 1) % 3
        if self.skill_heal >= 3 * 10:
            self.healer.state_machine.cur_state = self.healer_idle
            self.healer_idle.enter(None)

    def draw(self):
        self.image.clip_draw(self.healer.frame * 100 ,0, 100, 100, self.healer.x, self.healer.y)
    pass

class healer:
    def __init__(self):
        self.x, self.y = 100, 210
        self.frame = 0
        self.hp = 110
        self.str = 20

        self.healer_idle = IDLE(self)
        self.healer_heal = HEAL(self)
        self.healer_run = RUN(self)

        self.state_machine = StateMachine (
            self.healer_run,
            {
                self.healer_idle: {space_down : self.healer_heal},
                self.healer_heal: {space_down : self.healer_idle},
                self.healer_run : {}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def use_skill(self):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.healer_heal
        self.healer_heal.enter(None)

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
