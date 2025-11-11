from pico2d import *
import random

import game_world
from boss import boss
from warrior import warrior
from enemy import enemy



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.type == SDLK_SPACE:
            for game_object in world:
                game_object.state_machine.handle_event(('INPUT', event))


open_canvas()

def reset_world():

    global running
    running = True


    Warrior = warrior()
    world.append(Warrior)

    Boss = boss()
    world.append(Boss)

    Enemy = enemy()
    world.append(Enemy)

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