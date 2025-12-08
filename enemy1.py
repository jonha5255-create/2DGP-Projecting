from pico2d import *

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class enemy:
    def __init__(self):
        self.x, self.y = 1000, 180
        self.frame = 0
        self.hp = 100
        self.str = 10
        self.speed = 100

        self.image_run = load_image('enemy1.png')
        self.image_attack = load_image('enemy1 attack.png')
        self.current_image = self.image_run

        self.timer = 0.0
        self.dir = -1

        self.build_behavior_tree()


    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def update(self):
        self.bt.run()

    def draw(self):
        if self.current_image == self.image_attack:
            self.current_image.clip_draw(int(self.frame) * 37, 0, 37, 100, self.x, self.y, 60, 60)
        else:
            self.current_image.clip_draw(int(self.frame) * 37, 0, 37, 100, self.x, self.y, 60, 60)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))

    def get_nearest_hero(self):
        targets = [h for h in [heroes.warrior, heroes.healer, heroes.archer] if h]
        if not targets: return None
        return min(targets, key=lambda h: abs(h.x - self.x))

    def is_hero_nearby(self, r):
        target = self.get_nearest_hero()
        if target:
            distance = abs(target.x - self.x)
            if distance <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_to_hero(self):
        self.current_image = self.image_run
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 4
            self.timer = 0.0

        self.x += self.dir * self.speed * game_framework.frame_time
        return BehaviorTree.SUCCESS

    def attack_hero(self):
        self.current_image = self.image_attack

        # 공격 프레임 진행
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame += 1
            self.timer = 0

            # 공격 판정 (특정 프레임에서 데미지)
            if int(self.frame) == 6:  # 예: 3번 프레임에서 타격
                target = self.get_nearest_hero()
                if target and abs(target.x - self.x) < 60:
                    # 간단한 데미지 처리 (play_mode의 update에서 통합 처리해도 되지만 여기서 해도 됨)
                    # 여기서는 동작만 수행하고 실제 타격은 play_mode 충돌처리 충돌체크에 맡기거나,
                    # 직접 줄 수도 있음.
                    pass

                    # 애니메이션 종료 체크
        if self.frame >= 7:  # 공격 모션이 7프레임이라고 가정
            self.frame = 0
            return BehaviorTree.SUCCESS  # 공격 완료 -> 다시 판단

        return BehaviorTree.RUNNING  # 공격 중 -> 계속 실행

    def build_behavior_tree(self):
        # 1. 사거리(50) 안에 영웅이 있으면 -> 공격
        attack_node = Sequence("Attack",
                               Condition("In Range", self.is_hero_nearby, 50),
                               Action("Do Attack", self.attack_hero))

        # 2. 아니면 -> 이동
        move_node = Action("Move", self.move_to_hero)

        root = Selector("Root", attack_node, move_node)

        # 루트: 공격 시도해보고 안되면 이동
        self.bt = BehaviorTree(root)