from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP

import game_framework
import game_world
from effect import EFFECT
from state_machine import StateMachine
from enemy1 import enemy
from boss import boss

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector


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
        self.warrior = warrior
        self.image = load_image('warrior_attack.png')
        self.timer = 0.0

    def enter(self,count):
        self.warrior.frame = 0
        self.timer = 0.0
        self.attack_finished = False
        self.chain_count = count if isinstance(count, int) else 1

        scale = 1.0 + (count - 1) * 0.5

        effect_x = self.warrior.x + 80
        effect_y = self.warrior.y

        skill_effect = EFFECT(effect_x, effect_y, 'warrior_attack', scale)
        game_world.add_object(skill_effect, 2)

        print(f"워리어 {count}체인 공격 이펙트 발동!")


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
                self.warrior.state_machine.cur_state = self.warrior.warrior_run
                self.warrior.warrior_run.enter(None)

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
                self.warrior_idle: {},
                self.warrior_attack: {},
                self.warrior_run : {}
            }
        )

    def get_bb(self):
        left = self.x - 50
        right = self.x + 20
        bottom = self.y - 50
        top = self.y + 50
        return left, bottom, right, top

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def use_skill(self, count):
        self.state_machine.cur_state.exit(None)
        self.state_machine.cur_state = self.warrior_attack
        self.warrior_attack.enter(count)


    # BT

    def get_nearest_enemy(self):
        enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]
        if not enemies: return None
        return min(enemies, key=lambda e: abs(e.x - self.x))
