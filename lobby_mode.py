from pico2d import *
import game_framework
import play_mode

image = None

def init():
    global image
    image = load_image('lobby.png')

def finish():
    global image
    del image


def update():
    pass

def draw():
    clear_canvas()
    draw_rectangle(0,0,1600,800,0,0,0,255,1)
    image.draw(800,400,800,400)
    update_canvas()
    pass

def handle_events():
    event_list = get_events() # 버퍼로부터 모든 입력을 가지고 온다
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)


def pause(): pass
def resume(): pass