from pico2d import *

import game_framework


class stage2:
    def __init__(self):
        self.ground = load_image('stage2_ground.png')
        self.background = load_image('stage2_background.png')

        self.ground_width = self.ground.w
        self.background_width = self.background.w

        self.ground_x = 0
        self.background_x = 0

        self.ground_speed = 6
        self.background_speed = 4

    def draw(self):
        for i in range(3):
            self.background.draw(self.background_x + i * self.background_width, 350)

        for i in range(3):
            self.ground.draw(self.ground_x + i * self.ground_width, 350)

    def update(self):
        self.background_x -= self.background_speed * game_framework.frame_time * 50
        if self.background_x <= -self.background_width:
            self.background_x = 0

        self.ground_x -= self.ground_speed * game_framework.frame_time * 50
        if self.ground_x <= -self.ground_width:
            self.ground_x = 0
        pass
