from pico2d import *



class Skill_Pan:
    def __init__(self):
        self.image = load_image('Skill_Pan.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 200)