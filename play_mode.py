from pico2d import *
import random

import lobby_mode
import level_manager

from archer import archer
from healer import healer
from archer import archer
from stage1 import stage1
from stage2 import stage2
from stage3 import stage3
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

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for i, block in enumerate(skill_blocks):
                skill_type = block.handle_event(event)
                if skill_type:
                    # 연결된 블록 인덱스와 개수 구하기
                    connected_indices, count = SKILLBLOCK.find_connected_skill(skill_blocks, i)
                    if count >= 1:
                        # 연결된 블록들에 효과 적용 및 제거
                        for idx in sorted(connected_indices, reverse=True):
                            removed_block = skill_blocks.pop(idx)
                            game_world.remove_object(removed_block)
                        # 스킬 효과 적용 (예시)
                        if skill_type == 'warrior':
                            Warrior.use_skill(count)
                        elif skill_type == 'archer':
                            Archer.use_skill(count)
                        elif skill_type == 'healer':
                            Healer.use_skill(count)
                        # 인덱스 재정렬
                        for j, block in enumerate(skill_blocks):
                            block.reset_target(j)
                    break

            # 캐릭터 및 보스 이벤트 처리
            Warrior.handle_event(event)
            Healer.handle_event(event)
            Archer.handle_event(event)
            Boss.handle_event(event)

def add_skill_block():
    if len(skill_blocks) < MAX_SKILL_BLOCK:
        new_block = SKILLBLOCK(len(skill_blocks))
        skill_blocks.append(new_block)
        game_world.add_object(new_block, 1)
        print(f"블록 추가: index={len(skill_blocks) - 1}, target_x={new_block.target_x}")  # 디버깅
        return new_block
    return None





def init():
    global Warrior, Healer, Archer, Boss
    global skill_blocks

    skill_blocks = []

    level_mgr = level_manager.LEVEL_MANAGER()
    stage = level_mgr.get_current_stage()
    game_world.add_object(stage, 1)

    Warrior = warrior()
    game_world.add_object(Warrior, 1)

    Healer = healer()
    game_world.add_object(Healer, 1)

    Archer = archer()
    game_world.add_object(Archer, 1)


    level_mgr.spawn_wave()

    Skill_pan = skill_pan()
    game_world.add_object(Skill_pan, 0)


    add_skill_block()


def update():
    game_world.update()

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
    game_world.clear()

def pause(): pass
def resume(): pass
