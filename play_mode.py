from pico2d import *
import random

import lobby_mode
from level_manager import LEVEL_MANAGER
import heroes

from healer import healer
from archer import archer
from warrior import warrior
from boss import boss
from enemy1 import enemy
from skill_pan import skill_pan
from skill_block import SKILLBLOCK

import game_world
import game_framework


skill_blocks = []
MAX_SKILL_BLOCK = 9
level_mgr = None


def handle_events():
    global skill_blocks
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for i, block in enumerate(skill_blocks):
                skill_type = block.handle_event(event)

                if skill_type :
                    connected_indices, count = SKILLBLOCK.find_connected_skill(skill_blocks, i)

                    if count >= 1:
                        # heroes.py의 객체를 사용하여 스킬 발동
                        if skill_type == 'warrior':
                            heroes.warrior.use_skill(count)
                        elif skill_type == 'archer':
                            heroes.archer.use_skill(count)
                        elif skill_type == 'healer':
                            heroes.healer.use_skill(count)

                        # 블록 제거
                        for idx in sorted(connected_indices, reverse=True):
                            removed_block = skill_blocks.pop(idx)
                            game_world.remove_object(removed_block)

                        # 남은 블록 재정렬
                        for j, block in enumerate(skill_blocks):
                            block.reset_target(j)



            # 캐릭터 이벤트 처리
            heroes.warrior.handle_event(event)
            heroes.healer.handle_event(event)
            heroes.archer.handle_event(event)

def add_skill_block():
    if len(skill_blocks) < MAX_SKILL_BLOCK:
        new_block = SKILLBLOCK(len(skill_blocks))
        skill_blocks.append(new_block)
        game_world.add_object(new_block, 1)
        print(f"블록 추가: index={len(skill_blocks) - 1}, target_x={new_block.target_x}")  # 디버깅
        return new_block
    return None


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def init():
    global warrior, Healer, Archer, Boss
    global skill_blocks, level_mgr

    skill_blocks = []

    level_mgr = LEVEL_MANAGER()
    stage = level_mgr.get_current_stage()
    game_world.add_object(stage, 0)

    Skill_pan = skill_pan()
    game_world.add_object(Skill_pan, 1)


    heroes.warrior = warrior()
    game_world.add_object(heroes.warrior, 1)

    heroes.healer = healer()
    game_world.add_object(heroes.healer, 1)

    heroes.archer = archer()
    game_world.add_object(heroes.archer, 1)


    level_mgr.spawn_wave()


    add_skill_block()


def update():
    game_world.update()

    status = LEVEL_MANAGER.update(level_mgr)

    if skill_blocks and skill_blocks[-1].has_arrived():
        if len(skill_blocks) < MAX_SKILL_BLOCK:
            add_skill_block()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    global skill_blocks
    skill_blocks = []
    heroes.warrior = None
    heroes.healer = None
    heroes.archer = None
    game_world.clear()

def pause(): pass
def resume(): pass
