from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import game_world

from state_machine import StateMachine

class ATTACK:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image('boss attack.png')

    def enter(self):
        self.boss.frame = 0

    def exit(self):
        pass

    def do(self):
        pass

    def update(self):
        self.boss.frame = (self.boss.frame + 1) % 8

    def draw(self):
        frame_x = (self.boss.frame % 3) * 113
        frame_y = (2-(self.boss.frame // 3)) * 113
        self.image.clip_draw(frame_x,frame_y, 113, 113, self.boss.x, self.boss.y, 300, 300)
        #파일 안에 이미지 불러오기


class IDLE:
    def __init__(self, boss):
        self.boss = boss
        self.image = load_image('boss idle.png')

    def enter(self):
        self.boss.frame = 0

    def exit(self):
        pass

    def do(self):
        pass

    def update(self):
        self.boss.frame = (self.boss.frame + 1) % 4

    def draw(self):
        frame_x = (self.boss.frame % 2) * 113
        frame_y = (self.boss.frame // 2) * 113
        self.image.clip_draw(frame_x,frame_y, 113, 113, self.boss.x, self.boss.y, 300, 300)
        #파일 안에 이미지 불러오기


class boss:
    def __init__(self):
        self.x, self.y = 1300, 200
        self.frame = 0

        self.boss_idle = IDLE(self)
        self.boss_attack = ATTACK(self)
        self.state_machine = self.boss_idle #초기 상태 설정

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))