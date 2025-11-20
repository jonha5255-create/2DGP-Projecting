from pico2d import *



class skill_pan:
    def __init__(self):
        self.image = load_image('Skill_Pan.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(650, 50, 1300,100)