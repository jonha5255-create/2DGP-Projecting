from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP

import game_framework
import game_world
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class RUN:
    def __init__(self, healer):
        self.healer = healer
        self.image = load_image('healer run.png')
        self.timer = 0.0

    def enter(self,e):
        self.healer.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.healer.frame = (self.healer.frame + 1) % 2
            self.timer = 0.0


    def draw(self):
        self.image.clip_draw(self.healer.frame * 100 ,0, 100, 100, self.healer.x, self.healer.y)


class IDLE:
    def __init__(self,healer):
        self.healer = healer
        self.image = load_image('healer idle.png')
        self.timer = 0.0

    def enter(self,e):
        self.healer.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.healer.frame = (self.healer.frame + 1) % 2
            self.timer = 0.0

    def draw(self):
        self.image.clip_draw(self.healer.frame * 100 ,0, 100, 100, self.healer.x, self.healer.y)

class HEAL:
    def __init__(self, healer):
        self.healer_frame = None
        self.healer = healer
        self.image = load_image('healer heal.png')
        self.timer = 0.0

    def enter(self,e):
        self.healer.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.healer.frame = (self.healer.frame + 1) % 3
            self.timer = 0.0
        # 스킬 애니메이션이 끝나면 RUN으로 복귀
        if self.healer_frame == 2:
            self.healer.state_machine.cur_state = self.healer.healer_idle
            self.healer.healer_run.enter(None)

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

    def get_bb(self):
        left = self.x - 30
        right = self.x + 30
        bottom = self.y - 50
        top = self.y + 30
        return left, bottom, right, top

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def use_skill(self):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.healer_heal
        self.healer_heal.enter(None)

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
