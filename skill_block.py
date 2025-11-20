from pico2d import *

class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90

    def __init__(self):
        self.image = load_image('skill_block.png')
        self.x, self.y = 700, 90

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass