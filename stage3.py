from pico2d import *

import game_framework


class stage3:
    def __init__(self):
        self.background = load_image('stage3_background.png')
        self.ground = load_image('stage3_ground.png')
        self.sky = load_image('stage3_sky.png')
        self.moon = load_image('stage3_moon.png')

        self.ground_width = self.ground.w
        self.sky_width = self.sky.w
        self.background_width = self.background.w
        self.moon_width = self.moon.w // 2

        self.ground_x = 0
        self.sky_x = 0
        self.background_x = 0
        self.moon_x = 3.0  # 달의 초기 위치를 오른쪽으로 설정

        self.ground_speed = 4
        self.sky_speed = 2
        self.background_speed = 6
        self.moon_speed = 0.05

    def draw(self):
        # background (뒤쪽)
        for i in range(3):
            self.background.draw(self.background_x + i * self.background_width, 350)

        # sky (중간)
        for i in range(3):
            self.sky.draw(self.sky_x + i * self.sky_width, 350)

        self.moon.draw(self.moon_x * self.moon_width, 350)

        # ground (앞쪽)
        for i in range(3):
            self.ground.draw(self.ground_x + i * self.ground_width, 350)

    def update(self):
        ft = game_framework.frame_time * 50

        self.ground_x -= self.ground_speed * ft
        if self.ground_x <= -self.ground_width:
            self.ground_x = 0

        self.sky_x -= self.sky_speed * ft
        if self.sky_x <= -self.sky_width:
            self.sky_x = 0

        self.background_x -= self.background_speed * ft
        if self.background_x <= -self.background_width:
            self.background_x = 0

        # 달은 오른쪽으로 이동하도록 하고 동일한 스케일과 래핑 처리 적용
        self.moon_x -= self.moon_speed * game_framework.frame_time
