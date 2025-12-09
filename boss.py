from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class boss:
    def __init__(self):
        self.x, self.y = 1100, 320
        self.frame = 0
        self.hp = 1000
        self.max_hp = self.hp
        self.str = 60
        self.speed = 60


        self.image_idle = load_image('boss idle.png')
        self.image_attack = load_image('boss attack.png')
        self.image_heal = load_image('boss heal.png')
        self.current_image = self.image_idle

        self.timer = 0.0
        self.is_attacking = False
        self.is_healing = False

        self.build_behavior_tree()


    def get_bb(self):
        left = self.x - 170
        right = self.x + 170
        bottom = self.y - 200
        top = self.y + 200
        return left, bottom, right, top

    def update(self):
        self.bt.run()

    def draw(self):
        frame_x = (self.frame % 3) * 113
        frame_y = (2 - (self.frame // 3)) * 113
        idle_frame_y = (self.frame // 2) * 113

        if self.current_image == self.image_idle:
            self.image_idle.clip_composite_draw(frame_x,idle_frame_y, 113, 113,0,'h', self.x, self.y, 500, 500)
        elif self.current_image == self.image_attack or self.current_image == self.image_heal:
            self.image_attack.clip_composite_draw(frame_x,frame_y, 113, 113,0,'h', self.x, self.y, 500, 500)

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
            if abs(target.x - (self.x - 100)) <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_attack(self):
        self.is_attacking = True
        self.current_image = self.image_attack

        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 8
            self.timer = 0.0

        if self.frame >= 8:
            self.frame = 0
            self.is_attacking = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def move(self):
        self.is_attacking = False
        self.current_image = self.image_idle
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.frame = (self.frame + 1) % 4
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
        heal_node = Sequence("힐",
                            Condition("피가 30퍼 미만인가", self.hp_row),
                                Action("힐 하기", self.do_heal))
        attack_node = Sequence("공격",
                        Condition("사거리 내에 영웅들이 있나", self.is_hero_in_range, 80),
                               Action("공격해라", self.do_attack))

        heal_or_attack = Selector("힐 또는 공격", heal_node, attack_node)


        move_node = Action("이동", self.move)

        root = Selector("힐이나 공격을 안하면 이동",heal_or_attack, move_node)

        self.bt = BehaviorTree(root)
        pass