import random
from pico2d import *
import game_world
import game_framework

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

        enemies = []

        if self.wave < 3:
            count = random.randint(4,6) + (self.stage -1)
            for i in range(count):
                mob = enemy()
                mob.x = 1100 + i * 30
                mob.hp = 150 + (self.stage * 20)
                game_world.add_object(mob, 1)
                enemies.append(mob)
        elif self.wave == 3:
            boss_mob = boss()
            boss_mob.x = 1300
            boss_mob.hp = 1000 + (self.stage * 100)
            game_world.add_object(boss_mob, 1)
            enemies.append(boss_mob)


    def update(self):
        live_enemies = [o for o in game_world.world[1] if isinstance(o, (enemy, boss))]

        if len(live_enemies) == 0 and not self.wave_cleared:
            self.wave_cleared = True
            self.clear_timer = 0.0

        if self.wave_cleared:
            self.clear_timer += game_framework.frame_time
            if self.clear_timer > 2.0:
                self.next_wave()

    def next_wave(self):
        self.wave += 1

        if self.wave > 3:
            self.stage += 1
            self.wave = 1
            print(f"Stage {self.stage} 시작!")
            if self.stage > 3:
                print("모든 스테이지 클리어!")
                quit(0)
            return "stage_cleared"

        self.spawn_wave()
        return "wave_started"