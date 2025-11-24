import random
from pico2d import *

import game_framework


class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90
    START_Y = 50
    SPACING = 5  # 블록 간 간격
    SPEED = 800.0
    SPAWN_DELAY = 0.25

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
        self.x = -self.BLOCK_WIDTH / 2
        self.y = self.START_Y


        self.target_x = 1170 - index * (self.BLOCK_WIDTH + self.SPACING)
        self.target_y = self.START_Y

        self.spawn_delay = index * self.SPAWN_DELAY
        self.elapsed_time = 0.0

        self.is_spawned = False
        self.is_moving = False

    def draw(self):
        if self.is_spawned:
            self.image.draw(self.x, self.y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def update(self):
        if not self.is_moving:
            return

        if self.x < self.target_x:
            move_distance = self.SPEED * game_framework.frame_time
            self.x += move_distance



        if self.x >= self.target_x:
            self.x = self.target_x
            self.is_moving = False

    def has_arrived(self):
        return not self.is_moving