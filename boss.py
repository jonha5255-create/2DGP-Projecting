from pico2d import load_image


class boss:
    def __init__(self):
        self.x, self.y = 600, 200
        self.frame = 0
        self.image = load_image('boss idle.png')
    def update(self):
        self.frame += 1
        self.frame = self.frame% 4

    def draw(self):
        frame_x = (self.frame % 2) * 113
        frame_y = (self.frame // 2) * 113
        self.image.clip_draw(frame_x,frame_y, 113, 113, self.x, self.y, 300, 300)
        #파일 안에 이미지 불러오기