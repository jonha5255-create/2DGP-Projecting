from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP

import game_framework
import game_world
import play_mode
from state_machine import StateMachine
from effect import EFFECT
import random

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ATTACK_RANGE_PIXEL = 3.0 * PIXEL_PER_METER

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def skill_trigger(e):
    return e[0] == 'SKILL_TRIGGER'

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
        self.is_skill = False  # 스킬인지 일반 평타인지 구분하는 플래그

    def enter(self, e):
        self.archer.frame = 0
        self.timer = 0.0

        # [중요] e가 정수(int)면 스킬 발동, 아니면 일반 공격
        if isinstance(e, int):
            self.is_skill = True
            chain_count = e
            print(f"아쳐 스킬 발동! (체인: {chain_count})")

            # --- 스킬 이펙트 생성 ---
            effect_x = self.archer.x + 50
            effect_y = self.archer.y
            scale = 1.0 + (chain_count - 1) * 0.25

            # effect.py에 'archer_arrow'가 등록되어 있어야 함
            arrow = EFFECT(effect_x, effect_y, 'archer_attack', scale)
            game_world.add_object(arrow, 2)

        else:
            self.is_skill = False
            # 일반 공격은 이펙트 없이 화살만 나가거나, 약한 이펙트 추가 가능
            print("아쳐 일반 공격")

    def exit(self, e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.archer.frame = (self.archer.frame + 1) % 3  # 프레임 수 확인 필요
            self.timer = 0.0

        if self.archer.frame == 3:

            if self.is_skill:
                self.archer.state_machine.cur_state = self.archer.archer_run
                self.archer.archer_run.enter(None)

            else:
                target = self.archer.get_nearest_enemy()
                if target and (0 < (target.x - self.archer.x) <= ATTACK_RANGE_PIXEL):
                    self.archer.frame = 0  # 계속 공격 (루프)
                else:
                    # 적이 없으면 RUN으로 복귀
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
                self.archer_idle: { skill_trigger : self.archer_attack},
                self.archer_attack: {skill_trigger : self.archer_attack , space_down : self.archer_idle},
                self.archer_run : {skill_trigger : self.archer_attack}
            }
        )

    def get_bb(self):
        left = self.x - 50
        right = self.x + 40
        bottom = self.y - 50
        top = self.y + 30
        return left, bottom, right, top

    # 적 찾기 함수
    def get_nearest_enemy(self):
        nearest_enemy = None
        min_dist = 99999

        for obj in game_world.world[1]:
            if hasattr(obj, 'hp') and obj.__class__.__name__ == 'enemy':
                dist = obj.x - self.x
                if dist > 0 and dist < min_dist:
                    min_dist = dist
                    nearest_enemy = obj
        return nearest_enemy

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def use_skill(self,count):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.archer_attack
        self.archer_attack.enter(count)


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
