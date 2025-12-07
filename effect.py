from pico2d import *
import game_framework
import game_world

class EFFECT:
    IMAGE_FILE = {
        'healer_heal': 'heal_effect.png',
        'warrior_attack': 'warrior_skill_effect.png',
        'archer_attack': 'archer_effect.png'
    }

    def __init__(self, effect_type, x, y, scale=1.0):
        self.image = load_image(self.IMAGE_FILE[effect_type])
        self.x = x
        self.y = y
        self.scale = scale
        self.timer = 0.0

        if effect_type == 'healer_heal':
            self.frame_count = 3
            self.duration = 0.3
            self.frame_width = 100
            self.frame_height = 100
            self.is_animated = True
        elif effect_type == 'warrior_attack':
            self.frame_count = 4
            self.duration = 0.4
            self.frame_width = 128
            self.frame_height = 100
            self.is_animated = True
        elif effect_type == 'archer_attack':
            self.frame_count = 3
            self.duration = 0.4
            self.frame_width = 120
            self.frame_height = 100
            self.is_animated = True

        self.current_frame = 0

    def update(self):
        pass
    def draw(self):
        pass
    def handle_event(self, event):
        pass

