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
        else:
            warrior.handle_event(event)


def reset_world():
    global warrior


    Warrior = warrior()
    game_world.add_object(Warrior)

    Boss = boss()
    game_world.add_object(Boss)

    Enemy = enemy()
    game_world.add_object(Enemy)




def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

running = True

open_canvas()
reset_world()

while running:
    handle_events()

    update_world()  # 객체들의 상호작용을 시뮬레이션 , 계산
    render_world()  # 객체들의 모습을 그린다.
    delay(0.1)

close_canvas()