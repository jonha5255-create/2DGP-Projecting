from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import heroes
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class boss:
    def __init__(self, boss):
        self.boss = boss
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
        frame_x = (self.boss.frame % 3) * 113
        frame_y = (2 - (self.boss.frame // 3)) * 113
        idle_frame_y = (self.boss.frame // 2) * 113

        if self.image_idle:
            self.image_idle.composite_draw(frame_x,idle_frame_y, 113, 113,0,'h', self.boss.x, self.boss.y, 500, 500)
        else:
            self.image_attack.composite_draw(frame_x,frame_y, 113, 113,0,'h', self.boss.x, self.boss.y, 500, 500)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    # BT

    def get_nearest_hero(self):
        target = [h for h in [heroes.warrior, heroes.healer, heroes.archer] if h]
        if not target: return None
        return min(target, key=lambda h: abs(h.x - self.x))

    def is_hero_in_range(self, r):
        target = self.get_nearest_hero()
        if target:
            if abs(target.x - self.x) <= r:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def do_attack(self):

        pass

    def move(self):
        pass

    def hp_row(self):
        pass

    def do_heal(self):
        pass

    def build_behavior_tree(self):
        pass