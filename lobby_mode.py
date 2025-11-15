from pico2d import *
import game_framework
import play_mode

from sdl2 import SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

def button_down(x, y, e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT
def quit_game(e):
    return e[0] == 'INPUT' and e[1].type == SDL_QUIT or (e[1].type == SDL_KEYDOWN and e[1].key == SDLK_ESCAPE)

image = None
button = None

def init():
    global image, button
    image = load_image('lobby.png')
    button = load_image('start_button.png')

def finish():
    global image
    del image


def update():
    pass

def draw():
    clear_canvas()
    draw_rectangle(0,0,1600,800,0,10,0,150,1)
    image.draw(800,400,800,500)
    button.draw(800, 100, 300, 200)
    update_canvas()
    pass

def handle_events():
    event_list = get_events() # 버퍼로부터 모든 입력을 가지고 온다
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.key == SDL_BUTTON_LEFT:
            x, y = event.x, 800 - event.y
            if 650 <= x <= 950 and 0 <= y <= 200:
                game_framework.change_mode(play_mode)


def pause(): pass
def resume(): pass