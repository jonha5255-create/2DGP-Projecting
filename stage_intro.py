from pico2d import *
import game_framework


class StageIntro:
    def __init__(self):
        self.timer = 0.0
        self.show_time = 3.0
        self.is_finished = False

        # 배경 이미지 로드 (제공해주신 이미지)
        self.image = load_image('game_intro.jpg')

        # 폰트 로드 (크기 80으로 설정)
        self.font = load_font('arial.ttf', 60)


    def update(self):
        self.timer += game_framework.frame_time
        if self.timer >= self.show_time:
            self.is_finished = True

    def draw(self):
        clear_canvas()

        # 캔버스 / 이미지 원본 크기
        cw = get_canvas_width()
        ch = get_canvas_height()
        iw = self.image.w
        ih = self.image.h



        # 중앙에 맞춰 그리기
        self.image.draw(cw//2, 300, 1300, 600)

        # 좌표 (150, 450) 위치가 왼쪽 여백 쯤입니다.
        if self.font:
            # 본 글씨 (흰색)
            self.font.draw(120, 450, "STAGE 1", (255, 255, 255))
            self.font.draw(120, 350, "FOREST", (255, 255, 255))
