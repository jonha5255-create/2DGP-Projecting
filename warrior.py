from pico2d import load_image


class warrior:
    def __init__(self):
        self.x, self.y = 100, 200
        self.frame = 0
        self.image = load_image('warrior idle.png')
    def update(self):
        self.frame += 1
        self.frame = (self.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.frame * 100 ,0, 100, 100, self.x, self.y)
        #파일 안에 이미지 불러오기