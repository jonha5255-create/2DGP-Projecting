from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

BOSS_DATA = {
    1: {'idle': 'stage1_boss.png', 'attack': 'stage1_boss_att.png','heal':None,
        'hp': 1000, 'speed': 40, 'str': 50,
        'w': 102, 'h': 106,'at_w':161, 'at_h':196,
        'idle_frame': 4, 'attack_frame': 4},
    2: {'idle': 'stage2_boss.png', 'attack': 'stage2_boss_att.png','heal':None,
        'hp': 1500, 'speed': 80, 'str': 70,
        'w': 49, 'h': 60,'at_w': 55, 'at_h': 70,
        'idle_frame': 4, 'attack_frame': 6},
    3: {'idle': 'boss idle.png', 'attack': 'boss attack.png', 'heal': 'boss heal.png',
        'hp': 2000, 'speed': 100, 'str': 90,
        'w': 113, 'h': 113,'at_w': 113, 'at_h': 113,
        'idle_frame': 4, 'attack_frame': 8, 'heal_frame': 8
        }
}

class boss:
    def __init__(self,stage_id=1):
        self.x, self.y = 1100, 320
        self.frame = 0
        self.timer = 0.0
        self.is_attacking = False
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

        self.idle_frame_count = data.get('idle_frame', 4)
        self.attack_frame_count = data.get('attack_frame', 4)
        self.heal_frame_count = data.get('heal_frame', 8)

        self.image_idle = load_image(data['idle'])
        self.image_attack = load_image(data['attack'])
        if data.get('heal'):
            self.image_heal = load_image(data.get('heal'))
        else:
            self.image_heal = None

        self.current_image = self.image_idle

        self.build_behavior_tree()


    def get_bb(self):
        left = self.x - self.w *2
        right = self.x + self.w *2
        bottom = self.y - (self.h *2)-50
        top = self.y + (self.h *2)+50
        return left, bottom, right, top

    def update(self):
        self.bt.run()

    def draw(self):

        if self.current_image == self.image_idle:
            self.image_idle.clip_composite_draw(int(self.frame)*self.w,0,self.w,
                                                self.h,0,'h', self.x, self.y, 400, 400)
        elif self.current_image == self.image_attack:
            self.image_idle.clip_composite_draw(int(self.frame)*self.w,0,self.w,
                                                self.h,0,'h', self.x, self.y, 400, 400)
        elif self.current_image == self.image_heal:
            self.image_idle.clip_composite_draw(int(self.frame)*self.w,0,self.w,
                                                self.h,0,'h', self.x, self.y, 400, 400)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    # BT

    def get_nearest_hero(self):
        target = [h for h in [heroes.warrior, heroes.healer, heroes.archer] if h]
        if not target: return None
        return min(target, key=lambda h: abs(h.x - self.x - 100))

    def is_hero_in_range(self, r):
        target = self.get_nearest_hero()
        if target:
            if abs(target.x - (self.x - 50)) <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_attack(self):
        self.is_attacking = True
        self.current_image = self.image_attack

        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % self.attack_frame_count
            self.timer = 0.0

        if self.frame >= self.attack_frame_count:
            self.frame = 0
            self.is_attacking = False
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

        self.timer += game_framework.frame_time
        if self.timer >= 0.2:
            self.frame = (self.frame + 1) % 8
            self.timer = 0.0

        if self.frame >= 8:
            self.frame = 0
            self.is_healing = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        attack_node = Sequence("공격",
                        Condition("사거리 내에 영웅들이 있나", self.is_hero_in_range, 70),
                               Action("공격해라", self.do_attack))
        if self.image_heal:
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