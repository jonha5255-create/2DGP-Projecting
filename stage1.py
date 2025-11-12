from pico2d import *

class stage1:
    def __init__(self):
        self.image = load_image('stage1_background.png')

    def draw(self):
        self.image.draw(450, 150)

    def update(self):
        pass