from pico2d import *

import game_framework
import game_world

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

    def exit(self,e):
        pass

    def do(self):
        self.timer += game_framework.frame_time
        if self.timer > 0.1:
            self.enemy.frame = (self.enemy.frame + 1) % 7
            self.timer = 0.0
        pass

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.enemy.frame * 37 ,0, 37, 100, self.enemy.x, self.enemy.y, 60, 60)
        draw_rectangle(*self.enemy.get_bb())


class IDLE:
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
        pass

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
        self.hp = 150
        self.str = 20

        self.enemy_idle = IDLE(self)
        self.enemy_attack = ATTACK(self)
        self.state_machine = StateMachine(
            self.enemy_idle,
            {
                self.enemy_attack : { 'INPUT': self.enemy_idle },
                self.enemy_idle : { 'INPUT': self.enemy_attack }
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