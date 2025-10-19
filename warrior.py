from pico2d import load_image
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_LEFT

from state_machine import StateMachine


class IDLE:
    def __init__(self,warrior):
        self.warrior = warrior
        self.frame = 0
        self.image = load_image('warrior idle.png')
    def update(self):
        self.warrior.frame += 1
        self.warrior.frame = (self.warrior.frame + 1) % 3
    def draw(self):
        self.image.clip_draw(self.warrior.frame * 100 ,0, 100, 100, self.warrior.x, self.warrior.y)

class ATTACK:
    def __init__(self,warrior):

        self.warrior = warrior
        self.warrior.frame = 0
        self.warrior.image = load_image('warrior attack.png')
    def update(self):
        self.warrior.frame += 1
        self.warrior.frame = (self.warrior.frame + 1) % 4
    def draw(self):
        self.image.clip_draw(self.warrior.frame * 100 ,0, 100, 100, self.warrior.x, self.warrior.y)
    pass

class warrior:
    def __init__(self):
        self.x, self.y = 100, 200
        self.frame = 0

        self.IDLE = IDLE(self)
        self.ATTACK = ATTACK(self)
        self.state_machine = StateMachine (
            self.IDLE,
            {
                self.IDLE : {('INPUT',): self.ATTACK},
                self.ATTACK : {('INPUT',): self.IDLE,}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()