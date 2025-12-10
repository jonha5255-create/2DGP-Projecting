from pico2d import *

import game_framework
import game_world
import heroes
from effect import EFFECT
from enemy1 import enemy
from boss import boss

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class healer:
    def __init__(self):
        self.x, self.y = 100, 205
        self.frame = 0
        self.hp = 250
        self.max_hp = self.hp
        self.str = 25
        self.speed = 80

        # healer 에셋으로 변경
        self.healer_idle = load_image('healer idle.png')
        self.healer_attack = load_image('healer heal.png')
        self.healer_heal = load_image('healer_skill.png')
        self.healer_run = load_image('healer run.png')
        self.current_image = self.healer_run

        self.skill_queue = 0  # 스킬 사용 대기열
        self.timer = 0.0
        self.is_attacking = False # 현재 공격 중인지 여부
        self.is_use_skill = False # 현재 스킬 사용 중인지 여부

        self.heal_sound = load_wav('heal_sound.wav')
        self.heal_sound.set_volume(32)

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 30, self.y - 60, self.x + 30, self.y + 20

    def update(self):
        self.bt.run()

    def draw(self):
        if self.current_image == self.healer_run:
            self.current_image.clip_draw(int(self.frame) * 100, 0 , 100, 100, self.x,self.y)
        elif self.current_image == self.healer_attack:
            self.current_image.clip_draw(int(self.frame) * 100, 0 , 100, 100, self.x,self.y)
        else:
            self.current_image.clip_draw(int(self.frame) * 100, 0 , 100, 100, self.x,self.y)

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

    # 스킬 사용
    def do_skill(self):
        self.is_attacking = True
        self.current_image = self.healer_attack
        if not self.is_use_skill:
            self.frame = 0
            self.timer = 0.0
            self.is_use_skill = True

            self.heal_sound.play()

            scale = 1.0
            heal_amount = self.str * self.skill_queue  # 기본 힐량 * 체인 수
            # EFFECT에 올바른 힐러 에셋 이름 사용
            party = [heroes.warrior, heroes.archer, heroes.healer]
            for member in party:
                if member:  # 살아있는 멤버만
                    if member.hp < member.max_hp:
                        member.hp += heal_amount
                        if member.hp > member.max_hp:
                            member.hp = member.max_hp
                    # 이펙트 생성
                    heal_effect = EFFECT(member.x, member.y, 'healer_heal', scale)
                    game_world.add_object(heal_effect, 2)

        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame += 1
            self.timer = 0.0

        # 스킬 끝나고 나면
        if self.frame >= 2:
            self.frame = 0
            self.skill_queue = 0 # 스킬 사용 후 대기열 초기화
            self.is_attacking = False
            self.is_use_skill = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    # 적이 사정거리 내에 있는지 확인
    def is_enemy_in_range(self, r):
        target = self.get_nearest_enemy()
        if target:
            target_body_size = getattr(target, 'w', 0)

            distance = abs(target.x - self.x) - target_body_size

            # 계산된 거리가 사거리(r)보다 작으면 공격
            if distance <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    # 일반 공격
    def do_attack(self):
        self.is_attacking = True
        self.current_image = self.healer_attack
        if int(self.frame) == 0 and self.timer == 0.0:
            ball = EFFECT(self.x + 10 , self.y, 'healer_attack', 0.5)
            game_world.add_object(ball, 2)

        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame += 1
            self.timer = 0.0

        if self.frame >= 2:
            self.frame = 0
            self.is_attacking = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move(self):
        self.is_attacking = False
        self.current_image = self.healer_run
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 2
            self.timer = 0.0

        if self.x < 600:
            self.x += self.speed * game_framework.frame_time
        elif self.x >= 600:
            self.x = 600
        return BehaviorTree.SUCCESS

    def move_back(self):
        self.is_attacking = False
        self.current_image = self.healer_run

        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 2
            self.timer = 0.0

        if self.x > 0:
            self.x -= self.speed * game_framework.frame_time
        elif self.x <= 0:
            self.x = 0
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        skill_node = Sequence("스킬",
                              Condition("트리거",self.check_skill_trigger),
                              Action("스킬발현",self.do_skill))

        back_move = Sequence("뒷 무빙",
                             Condition("적 가까운가", self.is_enemy_in_range, 150),
                             Action("뒤로 도망",self.move_back))

        attack = Sequence("공격",
                          Condition("사거리 내에 있는가", self.is_enemy_in_range, 300),
                          Action("공격하기", self.do_attack))

        skill_and_attack = Selector("스킬 또는 공격", skill_node, attack)


        move = Action("전진",self.move)

        move_or_back = Selector("이동 또는 뒷무빙", back_move, move)

        root = Selector("Root", skill_and_attack, move_or_back)

        self.bt = BehaviorTree(root)