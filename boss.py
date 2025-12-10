from pico2d import *

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

BOSS_DATA = {
    1: {'idle': 'stage1_boss.png', 'attack': 'stage1_boss_att.png','heal':None,
        'hp': 800, 'speed': 40, 'str': 45,
        'w': 102, 'h': 106,'at_w':161, 'at_h':196,
        'idle_frame': 4, 'attack_frame': 4,'face_right': True},
    2: {'idle': 'stage2_boss.png', 'attack': 'stage2_boss_att.png','heal':None,
        'hp': 1200, 'speed': 80, 'str': 60,
        'w': 49, 'h': 60,'at_w': 55, 'at_h': 70,
        'idle_frame': 4, 'attack_frame': 6,'face_right': False},
    3: {'idle': 'boss idle.png', 'attack': 'boss attack.png', 'heal': 'boss heal.png',
        'hp': 1600, 'speed': 100, 'str': 70,
        'w': 113, 'h': 113,'at_w': 113, 'at_h': 113,'heal_w':113,'heal_h':113,
        'idle_frame': 4, 'attack_frame': 8, 'heal_frame': 8,'face_right': True
        }
}

class boss:
    def __init__(self,stage_id=1):
        self.x, self.y = 1100, 320
        self.frame = 0
        self.timer = 0.0
        self.dir = -1
        self.is_attacking = False
        self.attack = False
        self.is_healing = False

        data = BOSS_DATA.get(stage_id, BOSS_DATA[1])

        self.hp = data['hp']
        self.max_hp = self.hp
        self.str = data['str']
        self.speed = data['speed']
        self.w = data['w']
        self.h = data['h']
        self.at_w = data['at_w']
        self.at_h = data['at_h']
        if data.get('heal_w'):
            self.heal_w = data['heal_w']
            self.heal_h = data['heal_h']

        self.idle_frame_count = data.get('idle_frame', 4)
        self.attack_frame_count = data.get('attack_frame', 4)
        self.heal_frame_count = data.get('heal_frame', 8)
        self.face = data.get('face_right', False)

        self.image_idle = load_image(data['idle'])
        self.image_attack = load_image(data['attack'])
        if data.get('heal'):
            self.image_heal = load_image(data.get('heal'))
        else:
            self.image_heal = None

        self.current_image = self.image_idle

        self.attack_sound = None
        self.heal_sound = None

        if stage_id == 3:
            self.attack_sound = load_wav('stage3_boss_sound.wav')
            self.attack_sound.set_volume(40)
            self.heal_sound = load_wav('boss_heal_sound.wav')
            self.heal_sound.set_volume(30)

        self.build_behavior_tree()


    def get_bb(self):
        left = self.x - (self.at_w *2)
        right = self.x + (self.w *2)
        bottom = self.y - (self.h *2)-50
        top = self.y + (self.h *2)
        return left, bottom, right, top

    def update(self):
        self.bt.run()

    def draw(self):
        flip = ''
        if self.dir == -1:
            if self.face:
                flip = 'h'
            else:
                flip = ''
        elif self.dir == 1:
            if self.face:
                flip = ''
            else:
                flip = 'h'


        if self.current_image == self.image_attack:
            self.image_attack.clip_composite_draw(int(self.frame)*self.at_w,0,self.at_w,
                                                self.at_h,0,flip, self.x, self.y, 400, 400)
        elif self.current_image == self.image_heal:
            self.image_heal.clip_composite_draw(int(self.frame)*self.heal_w,0,self.heal_w,
                                                self.heal_h,0,flip, self.x, self.y, 400, 400)
        else:
            self.image_idle.clip_composite_draw(int(self.frame) * self.w, 0, self.w,
                                                self.h, 0, flip, self.x, self.y, 400, 400)
        # 1. 위치 및 크기 설정
        bar_x = self.x
        bar_y = 550
        bar_len = 200  # 바 길이
        bar_thick = 15  # 바 두께 (선의 개수)

        # 2. 비율 계산
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 0: hp_ratio = 0
        if hp_ratio > 1: hp_ratio = 1

        # 3. 좌표 계산
        x_left = bar_x - (bar_len // 2)
        x_right = bar_x + (bar_len // 2)
        x_hp = x_left + (bar_len * hp_ratio)  # 현재 체력 지점

        # 4. 선을 겹쳐서 두께 만들기 (검정 배경선 + 빨강 체력선)
        for i in range(bar_thick):
            y_pos = bar_y + i  # 한 줄씩 위로 쌓음

            # (1) 배경 (회색/검정) - 전체 길이
            draw_line(x_left, y_pos, x_right, y_pos)

            # (2) 체력 (빨강) - 남은 체력만큼만
            draw_rectangle(x_left, y_pos, x_hp, y_pos)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    # BT

    def get_nearest_hero(self):
        target = [h for h in [heroes.warrior, heroes.healer, heroes.archer] if h]
        if not target: return None
        return min(target, key=lambda h: abs(h.x - self.x))

    def is_hero_in_range(self, r):
        if self.is_attacking:
            return BehaviorTree.SUCCESS
        target = self.get_nearest_hero()
        if target:
            if abs(target.x - self.x) <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_attack(self):
        self.is_attacking = True
        self.current_image = self.image_attack

        if int(self.frame) == 0 and self.timer == 0.0:
            # 스테이지 3 보스라면 special_sound(일반공격음) 재생
            if self.attack_sound:
                self.attack_sound.play()

        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame += 1
            self.timer = 0.0

            # 공격 판정 (특정 프레임에서 데미지)
            if int(self.frame) == 3 and self.attack == False:
                target = self.get_nearest_hero()
                # 영웅이 있고 사거리(200) 안에 있다면
                if target and abs(target.x - self.x) < 200:
                    target.hp -= self.str
                    if target.hp < 0:
                        target.hp = 0
                    self.attack = True

        if self.frame >= self.attack_frame_count:
            self.frame = 0
            self.is_attacking = False
            self.attack = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def move(self):
        self.is_attacking = False
        self.current_image = self.image_idle
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % self.idle_frame_count
            self.timer = 0.0

        self.x -= self.speed * game_framework.frame_time
        return BehaviorTree.SUCCESS

    def hp_row(self):
        if self.hp <= self.max_hp * 0.3:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_heal(self):
        self.is_healing = True
        self.current_image = self.image_heal

        if self.frame == 0 and self.timer == 0.0:
            print("자가 치유")
            self.hp += 30
            if self.hp > self.max_hp: self.hp = self.max_hp
        if self.heal_sound:
            self.heal_sound.play()
        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame = (self.frame + 1) % self.heal_frame_count
            self.timer = 0.0

        if self.frame >= self.heal_frame_count:
            self.frame = 0
            self.is_healing = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        attack_node = Sequence("공격",
                        Condition("사거리 내에 영웅들이 있나", self.is_hero_in_range, 200),
                               Action("공격해라", self.do_attack))
        if self.current_image == self.image_heal:
            heal_node = Sequence("힐",
                                 Condition("피가 30퍼 미만인가", self.hp_row),
                                 Action("힐 하기", self.do_heal))
            heal_or_attack = Selector("힐 또는 공격", heal_node, attack_node)
        else:
            heal_or_attack = attack_node

        move_node = Action("이동", self.move)

        root = Selector("힐이나 공격을 안하면 이동",heal_or_attack, move_node)

        self.bt = BehaviorTree(root)
        pass