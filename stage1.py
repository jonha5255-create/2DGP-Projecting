from pico2d import *

class stage1:
    def __init__(self):
        self.ground = load_image('stage1_background.png')
        self.water = load_image('stage1_backwater.png')
        self.cloud = load_image('stage1_backcloud.png')

        self.water_width = self.water.w
        self.cloud_width = self.cloud.w
        self.ground_width = self.ground.w

        self.water_x = 0
        self.cloud_x = 0
        self.ground_x = 0

        self.water_speed = 4
        self.cloud_speed = 2
        self.ground_speed = 6

    def draw(self):
        for i in range(3):
            self.cloud.draw(self.cloud_x + i * self.cloud_width, 350)

        for i in range(3):
            self.water.draw(self.water_x + i * self.water_width, 200)

        for i in range(3):
            self.ground.draw(self.ground_x + i * self.ground_width, 200)

    def update(self):
        self.water_x -= self.water_speed
        if self.water_x <= -self.water_width:
            self.water_x = 0

        self.cloud_x -= self.cloud_speed
        if self.cloud_x <= -self.cloud_width:
            self.cloud_x = 0

        self.ground_x -= self.ground_speed
        if self.ground_x <= -self.ground_width:
            self.ground_x = 0
        pass
