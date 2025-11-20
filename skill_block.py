import random

from pico2d import *

class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90
    START_X = 1170  # 최종 목표 x 좌표
    START_Y = 50   # 최종 목표 y 좌표
    SPACING = 10   # 블록 간 간격
    SPEED = 100     # 이동 속도

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

        # 시작 위치 (화면 왼쪽 밖)
        self.x = -self.BLOCK_WIDTH
        self.y = self.START_Y

        # 목표 위치 (오른쪽으로 쌓이도록)
        self.target_x = self.START_X + index * (self.BLOCK_WIDTH + self.SPACING)
        self.target_y = self.START_Y

        self.is_moving = True

    def draw(self):
        self.image.draw(self.x, self.y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def update(self):
        if self.is_moving:
            # 목표 위치로 이동
            if self.x < self.target_x:
                self.x += self.SPEED
                if self.x >= self.target_x:
                    self.x = self.target_x
                    self.is_moving = False