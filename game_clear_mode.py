from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_r
import game_framework
import lobby_mode  # 로비로 돌아가기 위해 필요

image = None

def init():
    global image
    image = load_image('game_clear.jpg')

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(650, 400,1300,600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_r: # r 키를 누르면 로비로 이동
                game_framework.change_mode(lobby_mode)