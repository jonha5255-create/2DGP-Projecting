from pico2d import load_image

class ATTACK:
    def __init__(self):
        self.boss = boss()
        self.image = load_image('boss attack.png')
    def update(self):
        self.boss.frame += 1
        self.boss.frame = self.boss.frame % 8

    def draw(self):
        frame_x = (self.boss.frame % 3) * 113
        frame_y = (self.boss.frame // 3) * 113
        self.image.clip_draw(frame_x,frame_y, 113, 113, self.boss.x, self.boss.y, 300, 300)
        #파일 안에 이미지 불러오기


class IDLE:
    def __init__(self):
        self.boss = boss()
        self.image = load_image('boss idle.png')
    def update(self):
        self.boss.frame += 1
        self.boss.frame = self.boss.frame% 4

    def draw(self):
        frame_x = (self.boss.frame % 2) * 113
        frame_y = (self.boss.frame // 2) * 113
        self.image.clip_draw(frame_x,frame_y, 113, 113, self.boss.x, self.boss.y, 300, 300)
        #파일 안에 이미지 불러오기


class boss:
    def __init__(self):
        self.x, self.y = 600, 200
        self.frame = 0

        self.boss_idle = IDLE(self)
        self.boss_attack = ATTACK(self)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))