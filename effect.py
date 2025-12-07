from pico2d import *
import game_framework
import game_world

class EFFECT:
    IMAGE_FILE = {
        'healer_heal': 'healer_att_effect.png',
        'warrior_attack': 'warrior_skill_effect.png',
        'archer_attack': 'archer_effect.png'
    }

    def __init__(self, effect_type, x, y, scale=1.0):
        self.image = load_image(self.IMAGE_FILE[effect_type])
        self.x = x
        self.y = y
        self.scale = scale
        self.timer = 0.0

    def update(self):
        pass
    def draw(self):
        pass
    def handle_event(self, event):
        pass

