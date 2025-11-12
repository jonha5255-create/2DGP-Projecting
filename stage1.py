from pico2d import *

class stage1:
    def __init__(self):
        self.ground = load_image('stage1_background.png')
        self.water = load_image('stage1_backwater.png')
        self.cloud = load_image('stage1_backcloud.png')

        self.water_x = 0
        self.cloud_x = 0
        self.ground_x = 0

        self.water_speed = 2
        self.cloud_speed = 1
        self.ground_speed = 3

    def draw(self):
        self.cloud.draw(self.cloud_x, 350)
        self.cloud.draw(self.cloud_x + 900, 350)

        self.water.draw(self.water_x, 200)
        self.water.draw(self.water_x + 900,200)

        self.ground.draw(self.ground_x, 200)
        self.ground.draw(self.ground_x + 900,200)

    def update(self):
        self.water_x -= self.water_speed
        if self.water_x <= -self.water.w:
            self.water_x = 0

        self.cloud_x -= self.cloud_speed
        if self.cloud_x <= -self.cloud.w:
            self.cloud_x = 0

        self.ground_x -= self.ground_speed
        if self.ground_x <= -self.ground.w:
            self.ground_x = 0

