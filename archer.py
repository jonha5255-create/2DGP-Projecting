from pico2d import load_image, draw_rectangle
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
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_run.png')
        self.timer = 0.0

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 2
            self.timer = 0.0

    def draw(self):
        self.image.clip_draw(self.archer.frame * 120 ,0, 120, 100, self.archer.x, self.archer.y)

class IDLE:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_idle.png')
        self.timer = 0.0

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 2
            self.timer = 0.0

    def draw(self):
        self.image.clip_draw(self.archer.frame * 120, 0, 120, 100, self.archer.x, self.archer.y)


class ATTACK:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_attack.png')
        self.archer_arrow = 0
        self.timer = 0.0

    def enter(self, e):
        self.archer.frame = 0
        self.archer_arrow = 0

    def exit(self, e):
        self.archer_arrow = 0

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 3
            self.timer = 0.0

        if self.archer.frame == 3:
            # 공격 끝나고 idle 상태로 복귀
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

    def get_bb(self):
        left = self.x - 50
        right = self.x + 40
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
        self.state_machine.cur_state = self.archer_idle
        self.archer_idle.enter(None)


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
