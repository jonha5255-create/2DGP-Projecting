from pico2d import *
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP

import game_framework
import game_world
from effect import EFFECT
from state_machine import StateMachine
from enemy1 import enemy
from boss import boss

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class warrior:
    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.hp = 350
        self.str = 35
        self.dir = 1
        self.speed = 100

        self.warrior_idle = load_image('warrior_idle.png')
        self.warrior_attack = load_image('warrior_attack.png')
        self.warrior_run = load_image('warrior_run.png')
        self.current_image = self.warrior_run

        self.skill_queue = 0  # 스킬 사용 대기열
        self.timer = 0.0

        self.build_behavior_tree()

    def get_bb(self):
        if self.current_image == self.image_attack:
            return self.x - 50, self.y - 50, self.x + 80, self.y + 50
        return self.x - 50, self.y - 50, self.x + 20, self.y + 50

    def update(self):
        self.bt.run()

    def draw(self):


        draw_rectangle(*self.get_bb())

    def use_skill(self, count):
        self.skill_queue = count


    # BT

    def get_nearest_enemy(self):
        enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]
        if not enemies: return None
        return min(enemies, key=lambda e: abs(e.x - self.x))

    def check_skill_available(self):
        if self.skill_queue > 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_skill(self):
        pass

    def is_enemy_in_range(self, r):
        pass

    def do_attack(self):
        pass

    def move(self):
        pass

    def build_behavior_tree(self):
        pass
