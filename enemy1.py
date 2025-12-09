from pico2d import *

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

MOB_DATA = {
    # === 스테이지 1 (숲) ===
    1: {'idle': 'enemy2.png', 'attack': 'enemy2 attack.png',
        'hp': 100, 'speed': 80,'str': 10,
        'w': 37, 'h': 37,'at_w': 37, 'at_h': 37,
        'idle_frame': 4, 'attack_frame': 7, 'face_right': False},
    2: {'idle': 'enemy3.png', 'attack': 'enemy3 attack.png',
        'hp': 150, 'speed': 70,'str': 5,
        'w': 38, 'h': 38, 'at_w': 38, 'at_h': 38,
        'idle_frame': 4, 'attack_frame': 6, 'face_right': False},
    3: {'idle': 'enemy_magic.png', 'attack': 'enemy_magic attack.png',
        'hp': 90, 'speed': 90,'str': 15,
        'w': 40, 'h': 42, 'at_w': 40, 'at_h': 42,
        'idle_frame': 4, 'attack_frame': 6, 'face_right': False},

    # === 스테이지 2 (화산) ===
    4: {'idle': 'stage2_mob.png', 'attack': 'stage2_mob_att.png',
        'hp': 200, 'speed': 60,'str': 15,
        'w': 90, 'h': 90,'at_w': 90, 'at_h': 90,
        'idle_frame': 12, 'attack_frame': 12, 'face_right': True},
    5: {'idle': 'stage2_mob2.png', 'attack': 'stage2_mob2_att.png',
        'hp': 220, 'speed': 80, 'str': 15,
        'w': 64, 'h': 64, 'at_w': 64, 'at_h': 64,
        'idle_frame': 4, 'attack_frame': 5, 'face_right': True},

    # === 스테이지 3 (성) ===
    6: {'idle': 'stage3_mob.png', 'attack': 'stage3_mob_att.png',
        'hp': 300, 'speed': 90, 'str': 15,
        'w': 60, 'h': 60,'at_w': 60, 'at_h': 60,
        'idle_frame': 4, 'attack_frame': 5, 'face_right': True},
    7: {'idle': 'stage3_mob2.png', 'attack': 'stage3_mob2_att.png',
        'hp': 250, 'speed': 130, 'str': 15,
        'w': 60, 'h': 60, 'at_w': 60, 'at_h': 60,
        'idle_frame': 4, 'attack_frame': 5, 'face_right': True},
    8: {'idle': 'stage3_mob2.png', 'attack': 'stage3_mob3_att.png',
        'hp': 250, 'speed': 130, 'str': 15,
        'w': 60, 'h': 60, 'at_w': 60, 'at_h': 60,
        'idle_frame': 4, 'attack_frame': 5, 'face_right': True}
}

class enemy:
    def __init__(self, type_id=1):
        self.x, self.y = 1200, 180
        self.frame = 0
        self.timer = 0.0
        self.dir = -1
        self.is_attacking = False

        data = MOB_DATA.get(type_id, MOB_DATA[1])

        self.hp = data['hp']
        self.max_hp = self.hp
        self.str = data['str']
        self.speed = data['speed']
        self.w = data['w']
        self.h = data['h']
        self.at_w = data['at_w']
        self.at_h = data['at_h']
        self.idle_frame_count = data.get('idle_frame', 4)
        self.attack_frame_count = data.get('attack_frame', 4)
        self.face = data.get('face_right', False)

        self.image_run = load_image(data['idle'])
        self.image_attack = load_image(data['attack'])
        self.current_image = self.image_run



        self.build_behavior_tree()


    def get_bb(self):
        return (self.x -self.w , self.y - self.h ,
                self.x +self.w, self.y + self.h )

    def update(self):
        self.bt.run()

    def draw(self):
        flip = ''
        if self.dir == -1:
            if self.face:flip = 'h'
            else: flip = ''
        elif self.dir == 1:
            if self.face:flip = ''
            else:flip = 'h'

        if self.current_image == self.image_attack:
            self.current_image.clip_composite_draw(int(self.frame) * self.at_w, 0,
                                                   self.at_w, self.at_h,0,flip,self.x, self.y, 80, 80)
        else:
            self.current_image.clip_composite_draw(int(self.frame) * self.w, 0,
                                                   self.w, self.h,0,flip,self.x, self.y, 80, 80)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    # BT

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
        self.is_attacking = False
        self.current_image = self.image_run
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % self.idle_frame_count
            self.timer = 0.0

        self.x += self.dir * self.speed * game_framework.frame_time
        return BehaviorTree.SUCCESS

    def attack_hero(self):
        self.is_attacking = True
        self.current_image = self.image_attack

        # 공격 프레임 진행
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame += 1
            self.timer = 0

            # 공격 판정 (특정 프레임에서 데미지)
            if int(self.frame) == 5:
                target = self.get_nearest_hero()
                if target and abs(target.x - self.x) < 60:
                    target.hp -= self.str
                    if target.hp < 0:
                        target.hp = 0
                    pass

        # 애니메이션 종료 체크
        if self.frame >= self.attack_frame_count:  # 공격 모션이 7프레임이라고 가정
            self.frame = 0
            self.is_attacking = False
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