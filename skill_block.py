import random
from pico2d import *

import game_framework


class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90
    START_Y = 50
    SPACING = 5  # 블록 간 간격
    SPEED = 800.0
    ACTIVATION_DELAY = 0.5

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

        self.is_spawned = True
        self.is_moving = True

        # 도착 여부
        self.arrived = False
        self.activation_timer = 0.0
        self.is_activated = False

    def draw(self):
        if self.is_spawned:
            self.image.draw(self.x, self.y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def update(self):
        if self.is_moving:
            if self.x < self.target_x:
                move_distance = self.SPEED * game_framework.frame_time
                self.x += move_distance

            if self.x >= self.target_x:
                self.x = self.target_x
                self.is_moving = False
                self.arrived = True

        # 블록이 도착이후 활성화 타이머
        elif self.arrived and not self.is_activated:
            self.activation_timer += game_framework.frame_time
            if self.activation_timer >= self.ACTIVATION_DELAY:
                self.is_activated = True

    def has_arrived(self):
        return self.arrived and self.is_activated