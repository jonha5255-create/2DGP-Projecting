import random
from pico2d import *

import game_framework

class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90
    START_Y = 50
    SPACING = 5
    SPEED = 1000

    JOB_SKILL = {
        'warrior': 'warrior_skill.png',
        'archer': 'archer_skill.png',
        'healer': 'healer_skill.png'
    }

    def __init__(self, index):
        random_job = random.choice(['warrior', 'archer', 'healer'])
        self.skill_type = random_job

        image_file = self.JOB_SKILL.get(random_job, 'warrior_skill.png')
        self.image = load_image(image_file)

        # 왼쪽 화면 밖에서 시작
        self.x = 0
        self.y = self.START_Y


        self.target_x = 1170 - index * (self.BLOCK_WIDTH + self.SPACING)
        self.target_y = self.START_Y

        self.is_spawned = True
        self.is_moving = True

    def draw(self):
        if self.is_spawned:
            self.image.draw(self.x, self.y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def update(self):
        if self.is_moving:
            if self.x <= self.target_x:
                move_distance = self.SPEED * game_framework.frame_time * 0.1
                self.x += move_distance

                if self.x >= self.target_x:
                    self.x = self.target_x
                    self.is_moving = False

    def has_arrived(self):
        return not self.is_moving