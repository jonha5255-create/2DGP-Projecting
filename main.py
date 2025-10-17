from pico2d import *
import random

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
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas()

def reset_world():

    global running
    running = True

    global world  # 모든 게임객체를 담을 수 있는 리스트
    world = []

    Warrior = warrior()
    world.append(Warrior)

    Boss = boss()
    world.append(Boss)

reset_world()

def update_world():
    for game_object in world:
        game_object.update()

def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()

while running:
    handle_events()

    update_world()  # 객체들의 상호작용을 시뮬레이션 , 계산
    render_world()  # 객체들의 모습을 그린다.
    delay(0.1)

close_canvas()