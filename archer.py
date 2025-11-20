from pico2d import load_image
from sdl2 import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_MOUSEBUTTONDOWN, SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP
import game_world
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


class IDLE:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_idle.png')

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.archer.frame = (self.archer.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.archer.frame * 100, 0, 100, 100, self.archer.x, self.archer.y)


class ATTACK:
    def __init__(self, archer):
        self.archer = archer
        self.image = load_image('archer_attack.png')

    def enter(self, e):
        self.archer.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.archer.frame = (self.archer.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.archer.frame * 100, 0, 100, 100, self.archer.x, self.archer.y)


class archer:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.hp = 180
        self.str = 45

        self.archer_idle = IDLE(self)
        self.archer_attack = ATTACK(self)
        self.state_machine = StateMachine(
            self.archer_idle,
            {
                self.archer_idle: {space_down: self.archer_attack},
                self.archer_attack: {space_down: self.archer_idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
