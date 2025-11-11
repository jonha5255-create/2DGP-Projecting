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


def init():
    global Warrior
    global running

    running = True

    Warrior = warrior()
    game_world.add_object(Warrior, 1)

    Boss = boss()
    game_world.add_object(Boss, 1)

    Enemy = enemy()
    game_world.add_object(Enemy, 1)




def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
