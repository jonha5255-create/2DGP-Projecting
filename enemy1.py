from pico2d import *

import game_framework
import game_world
import heroes

from state_machine import StateMachine

class ATTACK:
    enemy = None
    def __init__(self, enemy):
        self.enemy = enemy
        if enemy is None:
            self.image = load_image('enemy1 attack.png')
        self.timer = 0.0

    def enter(self,e):
        self.enemy.frame = 0
        self.timer = 0.0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer > 0.1:
            self.enemy.frame = (self.enemy.frame + 1) % 7
            self.timer = 0.0

        # 공격 동작이 한 사이클 끝나면
        if self.enemy.frame == 6:
            target = self.enemy.get_nearest_hero()
            # 여전히 적이 사거리에 있으면 -> 계속 공격 (frame 0으로 리셋)
            if target and abs(target.x - self.enemy.x) < 50:
                self.enemy.frame = 0
            else:
                # 적이 멀어졌거나 죽었으면 -> 다시 RUN
                self.enemy.state_machine.cur_state = self.enemy.enemy_run
                self.enemy.enemy_run.enter(None)

    def draw(self):
        self.image.clip_draw(self.enemy.frame * 37 ,0, 37, 100, self.enemy.x, self.enemy.y, 60, 60)
        draw_rectangle(*self.enemy.get_bb())


class RUN:
    def __init__(self, enemy):
        self.enemy = enemy
        self.image = load_image('enemy1.png')
        self.timer = 0.0

    def enter(self,e):
        self.enemy.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer >= 0.1:
            self.enemy.frame = (self.enemy.frame + 1) % 4
            self.timer = 0.0

        # 2. 이동 (왼쪽으로)
        self.enemy.x -= 100 * game_framework.frame_time  # 이동 속도

        # 3. 타겟 탐색 및 상태 전이
        target = self.enemy.get_nearest_hero()
        if target:
            # 사거리 50 픽셀 이내면 공격 상태로 전환
            if abs(target.x - self.enemy.x) < 50:
                self.enemy.state_machine.cur_state = self.enemy.enemy_attack
                self.enemy.enemy_attack.enter(None)

    def draw(self):
        self.image.clip_draw(self.enemy.frame * 37 ,0, 37, 100, self.enemy.x, self.enemy.y, 60, 60)
        draw_rectangle(*self.enemy.get_bb())

    def update(self):
        pass

    def update(self):
        pass


class enemy:
    def __init__(self):
        self.x, self.y = 1000, 180
        self.frame = 0
        self.hp = 100
        self.str = 10
        self.ATTACK_CLASS = ATTACK

        self.enemy_run = RUN(self)
        self.enemy_attack = ATTACK(self)

        self.state_machine = StateMachine(
            self.enemy_run,
            {
                self.enemy_attack : {},
                self.enemy_run : {}
            }
        )

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))