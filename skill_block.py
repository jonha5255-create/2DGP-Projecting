import random
from pico2d import *
from sdl2 import SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_framework


class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90
    START_Y = 50
    SPACING = 5  # 블록 간 간격
    SPEED = 500.0
    ACTIVATION_DELAY = 0.1

    JOB_SKILL = {
        'warrior': 'warrior_skill.png',
        'archer': 'archer_skill.png',
        'healer': 'healer_skill.png'
    }

    def __init__(self, index):
        random_job = random.choice(['warrior', 'archer', 'healer'])
        self.skill_type = random_job

        image_file = self.JOB_SKILL.get(random_job, 'warrior_skill.png')
        self.image = load_image(image_file)

        # 왼쪽 화면 밖에서 시작
        self.x = -self.BLOCK_WIDTH / 2
        self.y = self.START_Y

        self.target_x = 1170 - index * (self.BLOCK_WIDTH + self.SPACING)

        self.is_spawned = True
        self.is_moving = True

        # 도착 여부
        self.arrived = False
        self.activation_timer = 0.0
        self.is_activated = False

    def draw(self):
        if self.is_spawned:
            self.image.draw(self.x, self.y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)

    def update(self):
        if self.is_moving:
            if self.x < self.target_x:
                move_distance = self.SPEED * game_framework.frame_time
                self.x += move_distance * 2

            if self.x >= self.target_x:
                self.x = self.target_x
                self.is_moving = False
                self.arrived = True

        # 블록이 도착이후 활성화 타이머
        elif self.arrived and not self.is_activated:
            self.activation_timer += game_framework.frame_time
            if self.activation_timer >= self.ACTIVATION_DELAY:
                self.is_activated = True

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if not self.is_spawned or not self.is_activated:
                    return None

                # 마우스 좌표 변환
                mouse_x = event.x
                mouse_y = get_canvas_height() - event.y

                # 블록 영역 계산
                left = self.x - self.BLOCK_WIDTH / 2
                right = self.x + self.BLOCK_WIDTH / 2
                bottom = self.y - self.BLOCK_HEIGHT / 2
                top = self.y + self.BLOCK_HEIGHT / 2

                # 클릭 영역 확인
                if left <= mouse_x <= right and bottom <= mouse_y <= top:
                    self.is_spawned = False
                    return self.skill_type

        return None

    def has_arrived(self):
        return self.arrived and self.is_activated

    def reset_target(self, index):
        self.target_x = 1170 - index * (self.BLOCK_WIDTH + self.SPACING)
        self.is_moving = True
        self.arrived = False
        self.activation_timer = 0.0
        self.is_activated = False

    def find_connected_skill(skill_block_list, clicked_index):
        if not (0 <= clicked_index < len(skill_block_list)):
            return [], 0

        base_type = skill_block_list[clicked_index].skill_type
        connected_indices = [clicked_index]

        # 왼쪽 탐색
        i = clicked_index - 1
        while i >= 0 and len(connected_indices) < 3:
            if skill_block_list[i].skill_type == base_type:
                connected_indices.insert(0, i)
                i -= 1
            else:
                break

        # 오른쪽 탐색
        i = clicked_index + 1
        while i < len(skill_block_list) and len(connected_indices) < 3:
            if skill_block_list[i].skill_type == base_type:
                connected_indices.append(i)
                i += 1
            else:
                break

        return connected_indices, len(connected_indices)