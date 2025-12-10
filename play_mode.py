from pico2d import *
import random

import game_clear_mode
import game_over_mode
from stage_intro import StageIntro
from ui import UI
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
ui = None
bgm = None
stage_intro = None
game_state = 'INTRO'


def play_stage_bgm(stage_num):
    global bgm
    if bgm:
        del bgm

    # [수정] 파일명을 .mp3 에서 .wav 로 변경
    # 업로드하신 파일명: stage1_sound.wav, stage2_sound.wav, stage3_sound.wav
    file_name = f"stage{stage_num}_sound.wav"

    try:
        bgm = load_music(file_name)  # wav파일도 load_music으로 재생 가능합니다
        bgm.set_volume(15)
        bgm.repeat_play()
        print(f"BGM 재생: {file_name}")
    except:
        print(f"BGM 파일 없음: {file_name}")

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
                        if skill_type == 'warrior' and heroes.warrior:
                            heroes.warrior.use_skill(count)
                        elif skill_type == 'archer' and heroes.archer:
                            heroes.archer.use_skill(count)
                        elif skill_type == 'healer' and heroes.healer:
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
    global warrior, Healer, Archer, Boss, bgm
    global skill_blocks, level_mgr, ui, stage_intro, game_state

    skill_blocks = []
    ui = UI()

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

    play_stage_bgm(1)

    stage_intro = StageIntro()
    game_state = 'INTRO'


def update():
    global game_state

    if game_state == 'INTRO':
        stage_intro.update()
        if stage_intro.is_finished:
            game_state = 'PLAY'
        return

    game_world.update()
    status = level_mgr.update()

    if ui: ui.update()

    # 영웅들 다 죽으면 게임 오버
    if check_heroes_dead() == True:
        game_framework.change_mode(game_over_mode)
        return

    if status == "stage_changed":
        change_stage()
    elif status == "game_cleared":
        game_framework.change_mode(game_clear_mode)
        return


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
                    break

        elif eff.effect_type in ['warrior_attack', 'archer_skill']:
            for e in enemies:
                # [중요] 'hit_enemies'에 없는 적만 때림 (중복 타격 방지)
                if e not in eff.hit_enemies and collide(eff, e):

                    damage = 0

                    # 1. 워리어 스킬 데미지 계산
                    if eff.effect_type == 'warrior_attack' and heroes.warrior:
                        # 기본 공격력 * 스킬 배율(예: 2배) * 체인 보너스(scale)
                        damage = heroes.warrior.str * 3.0 * eff.scale
                        print(f"워리어 스킬 적중! 데미지: {damage}")

                    # 2. 아처 스킬 데미지 계산
                    elif eff.effect_type == 'archer_skill' and heroes.archer:
                        # 아처는 여러 발 맞을 수도 있지만 일단은 한 방 강력하게
                        damage = heroes.archer.str * 2.5 * eff.scale
                        print(f"아처 스킬 적중! 데미지: {damage}")

                    # 데미지 적용
                    e.hp -= damage

                    # [중요] 때린 적을 명단에 등록 -> 다시는 안 때림
                    eff.hit_enemies.append(e)

                    if e.hp <= 0:
                        game_world.remove_object(e)

    # (3) 워리어 공격 vs 적 충돌
    if heroes.warrior and heroes.warrior.is_attacking:
        if int(heroes.warrior.frame) == 2:  # 공격 타격 프레임 (예: 2)
            for e in enemies:
                # 이미 때린 적은 건너뜀 (not in)
                if e not in heroes.warrior.hit_enemies and collide(heroes.warrior, e):

                    e.hp -= heroes.warrior.str
                    heroes.warrior.hit_enemies.append(e)

                    if e.hp <= 0:
                        game_world.remove_object(e)


    check_heroes_dead()

    if skill_blocks and skill_blocks[-1].has_arrived():
        if len(skill_blocks) < MAX_SKILL_BLOCK:
            add_skill_block()





def check_heroes_dead():
    if heroes.warrior and heroes.warrior.hp <= 0:
        game_world.remove_object(heroes.warrior)
        heroes.warrior = None
    if heroes.archer and heroes.archer.hp <= 0:
        game_world.remove_object(heroes.archer)
        heroes.archer = None
    if heroes.healer and heroes.healer.hp <= 0:
        game_world.remove_object(heroes.healer)
        heroes.healer = None
    # 모두 죽으면 True 반환
    if heroes.warrior is None and heroes.archer is None and heroes.healer is None:
        return True

    return False

def change_stage():
    game_world.world[0] = []

    new_stage = level_mgr.get_current_stage()

    game_world.add_object(new_stage, 0)

    print("스테이지 변경됨")
    play_stage_bgm(level_mgr.stage)

def draw():
    clear_canvas()

    if game_state == 'INTRO':
        stage_intro.draw()  # 인트로 화면(검은 배경+이미지+글씨) 그리기
    else:
        # 게임 화면 그리기 (기존 코드)
        game_world.render()
        if ui: ui.draw()

    update_canvas()

def finish():
    global skill_blocks, ui, bgm
    skill_blocks = []
    heroes.warrior = None
    heroes.healer = None
    heroes.archer = None
    ui = None
    if bgm:
        del bgm
    game_world.clear()

def pause(): pass
def resume(): pass
