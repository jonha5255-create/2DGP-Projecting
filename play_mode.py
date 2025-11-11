from pico2d import *

from healer import healer
from warrior import warrior
from boss import boss
from enemy import enemy
import game_world

import game_framework

Warrior = None
Boss = None
Enemy = None

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Warrior.handle_event(event)


def init():
    global Warrior, Boss, Enemy, Healer


    Warrior = warrior()
    game_world.add_object(Warrior, 1)

    Healer = healer()
    game_world.add_object(Healer, 1)

    Boss = boss()
    game_world.add_object(Boss, 1)

    Enemy = enemy()
    game_world.add_object(Enemy, 1)




def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    delay(0.1)
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
