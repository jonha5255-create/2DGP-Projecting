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
        self.hp = 230
        self.str = 35
        self.dir = 1

        self.warrior_idle = load_image('warrior_idle.png')
        self.warrior_attack = load_image('warrior_attack.png')
        self.warrior_run = load_image('warrior_run.png')
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
        self.skill_queue = count


    # BT

    def get_nearest_enemy(self):
        enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]
        if not enemies: return None
        return min(enemies, key=lambda e: abs(e.x - self.x))

    def  check_skill_available(self):
        if self.skill_queue > 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
