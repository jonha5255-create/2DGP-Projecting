from pico2d import *
import game_world


class enemy:
    def __init__(self):
        self.x, self.y = 450, 180
        self.frame = 0
        self.image = load_image('enemy1.png')
    def update(self):
        self.frame += 1
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 37 ,0, 37, 100, self.x, self.y, 60, 60)
        #파일 안에 이미지 불러오기