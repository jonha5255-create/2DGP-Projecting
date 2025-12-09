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
        self.is_attacking = False # 현재 공격 중인지 여부

        self.build_behavior_tree()

    def get_bb(self):
        if self.current_image == self.image_attack:
            return self.x - 50, self.y - 50, self.x + 80, self.y + 50
        return self.x - 50, self.y - 50, self.x + 20, self.y + 50

    def update(self):
        self.bt.run()

    def draw(self):
        if self.current_image == self.warrior_run:
            self.current_image.clip_draw(int(self.frame) * 128, 0 , 128, 100, self.x,self.y)
        else:
            self.current_image.draw(int(self.frame) * 128, 0 , 128, 100, self.x,self.y)

        # 바운딩 박스
        draw_rectangle(*self.get_bb())

    def use_skill(self, count):
        self.skill_queue = count

    def handle_event(self, event):
        pass

    # BT

    def get_nearest_enemy(self):
        enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]
        if not enemies: return None
        return min(enemies, key=lambda e: abs(e.x - self.x))

    def check_skill_trigger(self):
        if self.skill_queue > 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_skill(self):
        self.is_attacking = True
        self.current_image = self.warrior_attack

        if self.frame == 0 and self.timer == 0.0:
            scale = 1.0 + (self.skill_queue - 1) * 0.5
            skill_effect = EFFECT(self.x + 80, self.y, 'warrior_attack', scale)
            game_world.add_object(skill_effect, 2)
            print (f"워리어 스킬 사용! (체인: {self.skill_queue})")

        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame += 1
            self.timer = 0.0

        # 스킬 끝나고 나면
        if self.frame >= 3:
            self.frame = 0
            self.skill_queue = 0 # 스킬 사용 후 대기열 초기화
            self.is_attacking = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    # 적이 사정거리 내에 있는지 확인
    def is_enemy_in_range(self, r):
        target = self.get_nearest_enemy()
        if target and target.x - self.x <= r:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    # 적 일반 공격
    def do_attack(self):
        self.is_attacking = True
        self.current_image = self.warrior_attack
        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame += 1
            self.timer = 0.0

        if self.frame >= 3:
            self.frame = 0
            self.is_attacking = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move(self):
        self.is_attacking = False
        self.current_image = self.warrior_run
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 2
            self.timer = 0.0

        if self.x < 1100:
            self.x += self.dir * self.speed * game_framework.frame_time
        elif self.x >= 1100:
            self.x = 1100
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        skill_node = Sequence("Skill",
                              Condition("Trigger",self.check_skill_trigger),
                              Action("Do Skill",self.do_skill))

        attack = Sequence("Attack",
                          Condition("In Range", self.is_enemy_in_range, 80),
                          Action("Do Attack", self.do_attack))
        skill_and_attack = Selector("Skill and Attack", skill_node, attack)


        move = Action("Move",self.move)

        root = Selector("Root", skill_and_attack, move)

        self.bt = BehaviorTree(root)