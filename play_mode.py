from pico2d import *
import random

from effect import EFFECT
import lobby_mode
from level_manager import *
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


def add_skill_block():
    if len(skill_blocks) < MAX_SKILL_BLOCK:
        new_block = SKILLBLOCK(len(skill_blocks))
        skill_blocks.append(new_block)
        game_world.add_object(new_block, 1)
        print(f"블록 추가: index={len(skill_blocks) - 1}, target_x={new_block.target_x}")  # 디버깅
        return new_block
    return None


def collide(a, b):
    # a나 b가 충돌 박스가 없으면 False
    if not hasattr(a, 'get_bb') or not hasattr(b, 'get_bb'):
        return False

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
    status = level_mgr.update()

    if status == "Stage Clear":
        change_stage()


    # 충돌 처리
    enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]

    # (2) 아쳐 화살(이펙트) vs 적 충돌
    # 이펙트는 Layer 2(혹은 1)에 있습니다. archer.py에서 add_object(arrow, 2) 확인
    effects = [o for o in game_world.world[2] if isinstance(o, EFFECT)]

    for eff in effects:
        if eff.effect_type == 'archer_attack' or eff.effect_type == 'healer_attack':  # 화살인 경우만
            for e in enemies:
                if collide(eff, e):
                    if heroes.archer:
                        e.hp -= heroes.archer.str  # 아쳐 공격력만큼 데미지
                    elif heroes.healer:
                        e.hp -= heroes.healer.str  # 힐러 공격력만큼 데미지
                    game_world.remove_object(eff)  # 화살 사라짐
                    if e.hp <= 0:
                        game_world.remove_object(e)
                    break  # 화살 하나당 적 하나만 맞춤 (관통 원하면 break 제거)

    # (3) 워리어 공격 vs 적 충돌
    if heroes.warrior and heroes.warrior.is_attacking:
        if heroes.warrior.frame == 2:  # 공격 모션 중 타격 프레임
            for e in enemies:
                if collide(heroes.warrior, e):
                    damage = heroes.warrior.str * game_framework.frame_time * 5
                    e.hp -= damage
                    if e.hp <= 0:
                        game_world.remove_object(e)


    # (4) 적 vs 영웅 충돌 (적이 공격할 때)
    current_heroes = [h for h in [heroes.warrior, heroes.healer, heroes.archer] if h]

    for e in enemies:
        if hasattr(e, 'is_attacking') and e.is_attacking:
            for h in current_heroes:
                if collide(e, h):
                    h.hp -= e.str * game_framework.frame_time
                    if h.hp <= 0:
                        game_world.remove_object(h)
                        if h == heroes.warrior:
                            heroes.warrior = None
                        elif h == heroes.archer:
                            heroes.archer = None
                        elif h == heroes.healer:
                            heroes.healer = None

    if skill_blocks and skill_blocks[-1].has_arrived():
        if len(skill_blocks) < MAX_SKILL_BLOCK:
            add_skill_block()

def change_stage():
    game_world.world[0] = []

    new_stage = level_mgr.get_current_stage()

    game_world.add_object(new_stage, 0)

    print("스테이지 변경됨")

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
