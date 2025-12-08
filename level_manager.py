import random
from pico2d import *
import game_world

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
        self.bg = None

    def get_current_stage(self):
        if self.stage == 1: return stage1()
        elif self.stage == 2: return stage2()
        elif self.stage == 3: return stage3()
        return stage1()

    def spawn_wave(self):
        enemies = []
        if self.wave < 3:
            count = random.randint(2,3) + (self.stage -1)
            for i in range(count):
                mob = enemy()
                mob.x = 1000 + i * 50
                mob.hp = enemy.hp + (self.stage * 20)
                game_world.add_object(mob, 1)
                enemies.append(mob)
        else:
            boss_mob = boss()
            boss_mob.x = 1100
            boss_mob.hp = boss.hp + (self.stage * 100)
            game_world.add_object(boss_mob, 1)
            enemies.append(boss_mob)

        self.wave_cleared = False
        return enemies

    def check_wave_status(self, dt):
        pass

    def next_stage(self):
        pass