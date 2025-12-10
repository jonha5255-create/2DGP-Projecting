from pico2d import *
import game_framework
import game_world

class EFFECT:
    IMAGE_FILE = {
        'healer_heal': 'heal_effect.png',
        'healer_attack': 'healer_att_effect.png',
        'warrior_attack': 'warrior_skill_eff.png',
        'archer_attack': 'archer_effect.png',
        'archer_skill' : 'archer_3chain_effect.png'
    }

    def __init__(self,x, y,effect_type, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.effect_type = effect_type # 이펙트 종류 저장
        self.timer = 0.0


        self.velocity_x = 0.0 # 이동 속도
        self.velocity_y = 0.0

        self.hit_enemies = []  # 충돌한 적 목록

        if effect_type == 'healer_heal':
            self.frame_count = 3
            self.duration = 0.3
            self.frame_width = 100
            self.frame_height = 100
            self.is_animated = True
        elif effect_type == 'healer_attack':
            self.frame_count = 1
            self.duration = 0.5
            self.frame_width = 228
            self.frame_height = 215
            self.is_animated = False
            self.velocity_x = 600
        elif effect_type == 'warrior_attack':
            self.frame_count = 1
            self.duration = 0.4
            self.frame_width = 54
            self.frame_height = 166
            self.is_animated = True
            self.velocity_y = -800
        elif effect_type == 'archer_attack':
            self.frame_count = 3
            self.duration = 2.0
            self.frame_width = 120
            self.frame_height = 100
            self.is_animated = True
            self.velocity_x = 600  # 화살 이동 속도 설정
        elif effect_type == 'archer_skill':
            self.frame_count = 5
            self.duration = 2.0
            self.frame_width = 130
            self.frame_height = 120
            self.is_animated = True


        self.current_frame = 0
        self.image = load_image(self.IMAGE_FILE[effect_type])
    def get_bb(self):
        if self.effect_type == 'archer_attack':
            return self.x -30, self.y -10, self.x +30, self.y +10
        if self.effect_type == 'archer_skill':
            return self.x-75, self.y-60, self.x+ 75, self.y +60
        if self.effect_type == 'healer_attack':
            return self.x -10, self.y- 10, self.x+ 10, self.y + 10
        if self.effect_type == 'warrior_attack':
            return self.x - 20, self.y - 80, self.x + 20, self.y + 80

        return 0,0,0,0

    def update(self):
        self.timer += game_framework.frame_time

        self.y += self.velocity_y * game_framework.frame_time

        if self.effect_type == 'warrior_attack':
            if self.y < 250:
                self.y = 250
                self.velocity_y = 0
                return

        # 이동 로직 (아쳐 화살, 힐러 공격)
        if self.velocity_x > 0:
            self.x += self.velocity_x * game_framework.frame_time

        if self.timer >= self.duration:
            game_world.remove_object(self)
            return

        if self.is_animated:
            rate = self.timer / 0.5  # 0.5초마다 루프 혹은 duration 기준
            if self.effect_type == 'archer_attack':
                self.current_frame = int(self.timer * 10) % self.frame_count
            else:
                rate = self.timer / self.duration
                self.current_frame = int(rate * self.frame_count)
                if self.current_frame >= self.frame_count:
                    self.current_frame = self.frame_count - 1
        else:
            self.scale = game_framework.frame_time * 0.5
        pass
    def draw(self):
        sx = self.current_frame * self.frame_width
        if self.effect_type == 'archer_skill':
            self.image.clip_draw(
                sx, 0, self.frame_width,self.frame_height,
                self.x ,self.y + 160,
                (self.frame_width * 4) * self.scale, (self.frame_height * 4) * self.scale)
        elif self.effect_type == 'healer_attack':
            self.image.clip_draw(
                sx, 0, self.frame_width,self.frame_height,
                self.x ,self.y ,
                self.frame_width/2, self.frame_height/2)
        elif self.effect_type == 'healer_heal':
            self.image.clip_draw(
                sx, 0, self.frame_width, self.frame_height,
                self.x, self.y,
                self.frame_width,self.frame_height
            )
        else:
            self.image.clip_draw(
            sx, 0, self.frame_width, self.frame_height,
            self.x, self.y,
            self.frame_width * self.scale,
            self.frame_height * self.scale
        )
    def handle_event(self, event):
        pass

