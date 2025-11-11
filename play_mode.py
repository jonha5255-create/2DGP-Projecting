from pico2d import *

from warrior import warrior
from boss import boss
from enemy import enemy
import game_world

import game_framework

warrior = None

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            warrior.handle_event(event)


def reset_world():
    global Warrior


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
