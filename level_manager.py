import random
from pico2d import *

import game_clear_mode
import game_world
import game_framework
import heroes

from enemy1 import enemy
from boss import boss
from stage1 import stage1
from stage2 import stage2
from stage3 import stage3

class LEVEL_MANAGER:
    def __init__(self):
        self.stage = 1
        self.wave = 1
        self.wave_cleared = False
        self.clear_timer = 0.0


    def get_current_stage(self):
        if self.stage == 1: return stage1()
        elif self.stage == 2: return stage2()
        elif self.stage == 3: return stage3()
        return stage1()

    def spawn_wave(self):
        self.wave_cleared = False
        self.clear_timer = 0.0

        # 일반 웨이브
        if self.wave < 3:
            count = 2 + self.wave
            for i in range(count):
                mob_type = 1  # 기본값

                # 스테이지별로 등장할 몹 번호 지정
                if self.stage == 1:
                    mob_type = random.choice([1, 2, 3])
                elif self.stage == 2:
                    mob_type = random.choice([4, 5])
                elif self.stage == 3:
                    mob_type = random.choice([6, 7, 8])

                # 해당 타입의 적 생성
                mob = enemy(mob_type)
                mob.x = 1100 + i * 100
                game_world.add_object(mob, 1)

        # 보스 웨이브
        else:
            print(f"Stage {self.stage} Boss Appeared!")

            #현재 스테이지 번호를 보스에게 전달
            boss_mob = boss(self.stage)
            game_world.add_object(boss_mob, 1)


    def update(self):
        live_enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]

        if len(live_enemies) == 0 and not self.wave_cleared:
            self.wave_cleared = True
            self.clear_timer = 0.0

        if self.wave_cleared:
            self.clear_timer += game_framework.frame_time
            if self.clear_timer > 2.0:
                return self.next_wave()
        return None

    def next_wave(self):
        if heroes.warrior:
            heroes.warrior.x = 300  # 워리어 초기 위치
            heroes.warrior.is_attacking = False  # 공격 상태 해제
            heroes.warrior.current_image = heroes.warrior.warrior_run  # 달리기 모션으로 변경

        if heroes.archer:
            heroes.archer.x = 200  # 아쳐 초기 위치
            heroes.archer.is_attacking = False
            heroes.archer.current_image = heroes.archer.archer_run

        if heroes.healer:
            heroes.healer.x = 100  # 힐러 초기 위치
            heroes.healer.is_attacking = False
            heroes.healer.current_image = heroes.healer.healer_run
        self.wave += 1

        if self.wave > 3:
            self.stage += 1
            self.wave = 1

            if self.stage > 3:
                print("모든 스테이지 클리어!")
                game_framework.change_mode(game_clear_mode)  # 게임 종료 또는 엔딩 상태로 전환
                return "stage_clear"
            print(f"Stage {self.stage} 시작!")
            self.spawn_wave()
            return "stage_changed"


        self.spawn_wave()
        return "wave_started"