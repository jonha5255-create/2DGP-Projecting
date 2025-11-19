from pico2d import *
import random

import lobby_mode
from healer import healer
from stage1 import stage1
from warrior import warrior
from boss import boss
from enemy1 import enemy
from skill_pan import skill_pan
import game_world
import game_framework


Warrior = None
Boss = None
Enemy1 = None
Healer = None
Stage1 = None
Skill_pan = None


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Warrior.handle_event(event)
            Healer.handle_event(event)
            Boss.handle_event(event)



def init():
    global Warrior, Boss, Enemy1, Healer, Stage1, Skill_pan


    Warrior = warrior()
    game_world.add_object(Warrior, 1)

    Healer = healer()
    game_world.add_object(Healer, 1)

    Boss = boss()
    game_world.add_object(Boss, 1)


    for _ in range(random.randint(1, 5)):
        Enemy1 = enemy()
        Enemy1.x = random.randint(800, 1000)
        game_world.add_object(Enemy1, 1)

    Skill_pan = skill_pan()
    game_world.add_object(Skill_pan, 1)

    Stage1 = stage1()
    game_world.add_object(Stage1, 0)



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
