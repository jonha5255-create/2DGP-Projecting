from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_a, SDLK_h

import game_framework
import game_world

from state_machine import StateMachine

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def h_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_h

class HEAL:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image('boss heal.png')
        self.timer = 0.0

    def enter(self,e):
        self.boss.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.boss.frame = (self.boss.frame + 1) % 8
            self.timer = 0.0

    def draw(self):
        frame_x = (self.boss.frame % 3) * 113
        frame_y = (2-(self.boss.frame // 3)) * 113
        self.image.clip_composite_draw(frame_x,frame_y, 113, 113,0,'h', self.boss.x, self.boss.y, 500, 500)
        #파일 안에 이미지 불러오기

class ATTACK:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image('boss attack.png')
        self.timer = 0.0

    def enter(self,e):
        self.boss.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.boss.frame = (self.boss.frame + 1) % 8
            self.timer = 0.0


    def draw(self):
        frame_x = (self.boss.frame % 3) * 113
        frame_y = (2-(self.boss.frame // 3)) * 113
        self.image.clip_composite_draw(frame_x,frame_y, 113, 113,0,'h', self.boss.x, self.boss.y, 500, 500)
        #파일 안에 이미지 불러오기


class IDLE:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image('boss idle.png')
        self.timer = 0.0

    def enter(self,e):
        self.boss.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.boss.frame = (self.boss.frame + 1) % 4
            self.timer = 0.0


    def draw(self):
        frame_x = (self.boss.frame % 2) * 113
        frame_y = (self.boss.frame // 2) * 113
        self.image.clip_composite_draw(frame_x,frame_y, 113, 113,0,'h', self.boss.x, self.boss.y, 500, 500)
        #파일 안에 이미지 불러오기


class boss:
    def __init__(self):
        self.x, self.y = 1100, 320
        self.frame = 0
        self.hp = 1000
        self.str = 60

        self.boss_idle = IDLE(self)
        self.boss_attack = ATTACK(self)
        self.boss_heal = HEAL(self)
        self.state_machine = StateMachine(
            self.boss_idle, #초기 상태 설정
            {
                self.boss_idle : {a_down : self.boss_attack, h_down : self.boss_heal},
                self.boss_attack : {a_down : self.boss_idle, h_down : self.boss_heal},
                self.boss_heal : {h_down : self.boss_idle,a_down : self.boss_attack}
            }
        )

    def get_bb(self):
        left = self.x - 170
        right = self.x + 170
        bottom = self.y - 200
        top = self.y + 200
        return left, bottom, right, top

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))