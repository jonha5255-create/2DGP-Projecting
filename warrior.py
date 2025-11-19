from pico2d import load_image
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP
import game_world
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE




class IDLE:
    def __init__(self,warrior):
        self.warrior = warrior
        self.image = load_image('warrior idle.png')

    def enter(self,e):
        self.warrior.frame = 0

    def exit(self,e):
        pass

    def do(self):
       self.warrior.frame = (self.warrior.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.warrior.frame * 100 ,0, 100, 100, self.warrior.x, self.warrior.y)

class ATTACK:
    def __init__(self, warrior):
        self.warrior = warrior
        self.image = load_image('warrior attack.png')

    def enter(self,e):
        self.warrior.frame = 0

    def exit(self,e):
        pass

    def do(self):
        self.warrior.frame = (self.warrior.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.warrior.frame * 100 ,0, 100, 100, self.warrior.x, self.warrior.y)

class warrior:
    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.hp = 230
        self.str = 35

        self.warrior_idle = IDLE(self)
        self.warrior_attack = ATTACK(self)
        self.state_machine = StateMachine (
            self.warrior_idle,
            {
                self.warrior_idle: {space_down : self.warrior_attack},
                self.warrior_attack: {space_down : self.warrior_idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
