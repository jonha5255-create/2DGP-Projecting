from pico2d import *
import game_world

from state_machine import StateMachine

class ATTACK:
    def __init__(self, enemy):
        self.enemy = enemy
        self.image = load_image('enemy1 attack.png')

    def enter(self,e):
        self.enemy.frame = 0

    def exit(self,e):
        pass

    def do(self):
        pass

    def update(self):
        self.enemy.frame = (self.enemy.frame + 1) % 7

    def draw(self):
        self.image.clip_draw(self.enemy.frame * 37 ,0, 37, 100, self.enemy.x, self.enemy.y, 60, 60)


class IDLE:
    def __init__(self, enemy):
        self.enemy = enemy
        self.image = load_image('enemy1.png')

    def enter(self,e):
        self.enemy.frame = 0

    def exit(self,e):
        pass

    def do(self):
       pass

    def draw(self):
        self.image.clip_draw(self.enemy.frame * 37 ,0, 37, 100, self.enemy.x, self.enemy.y, 60, 60)

    def update(self):
        pass

    def update(self):
        self.enemy.frame = (self.enemy.frame + 1) % 4


class enemy:
    def __init__(self):
        self.x, self.y = 1200, 180
        self.frame = 0

        self.enemy_idle = IDLE(self)
        self.enemy_attack = ATTACK(self)
        self.state_machine = self.enemy_attack

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))