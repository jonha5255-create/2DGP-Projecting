from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP

import game_framework
import game_world
from state_machine import StateMachine
import random

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ATTACK_RANGE_PIXEL = 3.0 * PIXEL_PER_METER

def block_clicked(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT


class SKILL:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_attack.png')
        self.timer = 0.0

    def enter(self, e):
        self.archer.frame = 0
        self.timer = 0.0
        if isinstance(e, tuple) and len(e) > 2:
            self.chain_count = e[2]
        else:
            self.chain_count = 1
        print(f"Skill activated with chain count: {self.chain_count}")

    def exit(self, e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 4
            self.timer = 0.0

    def draw(self):
        self.image.clip_draw(self.archer.frame * 120, 0, 120, 100, self.archer.x, self.archer.y)
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

        self.archer.x += RUN_SPEED_PPS * game_framework.frame_time
        self.archer.x += clamp(0, self.archer.x,800)

        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 2
            self.timer = 0.0

        target = self.archer.get_nearest_enemy()
        if target:
            distance = target.x - self.archer.x
            if 0 < distance <= ATTACK_RANGE_PIXEL:
                self.archer.state_machine.cur_state = self.archer.archer_idle
                self.archer.archer_idle.enter(None)
                return

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
        self.timer = 0.0

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 3
            self.timer = 0.0

        if self.archer.frame == 2:
            target = self.archer.get_nearest_enemy()
            if target and (0 < (target.x - self.archer.x) <= ATTACK_RANGE_PIXEL):
                self.archer.frame = 0  # 계속 공격
            else:
                # 적이 없으면 바로 RUN 상태로 복귀
                self.archer.state_machine.cur_state = self.archer.archer_run
                self.archer.archer_run.enter(None)

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
