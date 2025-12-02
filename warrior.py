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
    def __init__(self, warrior):
        self.warrior = warrior
        self.image = load_image('warrior_run.png')
        self.timer = 0.0

    def enter(self,e):
        self.warrior.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.warrior.frame = (self.warrior.frame + 1) % 2
            self.timer = 0.0
        sx = RUN_SPEED_KMPH * game_framework.frame_time * 2.0
        self.warrior.x += sx

    def draw(self):
        self.image.clip_draw(self.warrior.frame * 128 ,0, 128, 100, self.warrior.x, self.warrior.y)




class IDLE:
    def __init__(self,warrior):
        self.warrior = warrior
        self.image = load_image('warrior_idle.png')
        self.timer = 0.0

    def enter(self,e):
        self.warrior.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.warrior.frame = (self.warrior.frame + 1) % 2
            self.timer = 0.0

    def draw(self):
        self.image.clip_draw(self.warrior.frame * 128 ,0, 128, 100, self.warrior.x, self.warrior.y)

class ATTACK:
    def __init__(self, warrior):
        self.attack_finished = None
        self.warrior = warrior
        self.image = load_image('warrior_attack.png')
        self.timer = 0.0

    def enter(self,e):
        self.warrior.frame = 0
        self.attack_finished = False

    def exit(self,e):
        pass

    def do(self):
        if not self.attack_finished:
            self.timer += game_framework.frame_time
            if self.timer >= 0.2:
                self.warrior.frame = (self.warrior.frame + 1) % 3
                self.timer = 0.0
            if self.warrior.frame == 2:
                self.attack_finished = True
                # 공격 끝나고 idle 상태로 복귀
                self.warrior.state_machine.cur_state = self.warrior.warrior_idle
                self.warrior.warrior_idle.enter(None)

    def draw(self):
        self.image.clip_draw(self.warrior.frame * 128 ,0, 128, 100, self.warrior.x, self.warrior.y)

class warrior:
    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.hp = 230
        self.str = 35
        self.dir = 1

        self.warrior_idle = IDLE(self)
        self.warrior_attack = ATTACK(self)
        self.warrior_run = RUN(self)
        self.state_machine = StateMachine (
            self.warrior_run,
            {
                self.warrior_idle: {space_down : self.warrior_attack},
                self.warrior_attack: {space_down : self.warrior_idle},
                self.warrior_run : {}
            }
        )

    def get_bb(self):
        left = self.x - 64
        right = self.x + 64
        bottom = self.y - 50
        top = self.y + 50
        return left, bottom, right, top

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def use_skill(self):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.warrior_attack
        self.warrior_attack.enter(None)



    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
