from pico2d import *
import heroes


class UI:
    def __init__(self):
        # 1. 폰트 로드 (프로젝트 폴더에 ttf 파일이 있어야 함)
        # 없으면 윈도우 폰트 폴더에서 Arial.ttf 등을 복사해오세요.
        # 파일명이 다르면 수정해야 합니다.
        try:
            self.font = load_font('Consolas.ttf', 16)
        except:
            self.font = None
            # 2. 직업별 UI 이미지 로드
        self.images = {
            'Warrior': load_image('warrior_ui.png'),
            'Archer': load_image('archer_ui.png'),
            'Healer': load_image('healer_ui.png')
        }

        # UI 배치 설정 (왼쪽 상단)
        self.start_x = 40
        self.start_y = 570
        self.gap = 170  # 캐릭터 슬롯 간격

    def update(self):
        pass

    def draw(self):
        # 파티 순서대로 그리기 (워리어 -> 힐러 -> 아쳐)
        # heroes 모듈에 있는 객체들을 리스트로 묶어서 처리
        party = [
            (heroes.warrior, 'Warrior'),
            (heroes.healer, 'Healer'),
            (heroes.archer, 'Archer')
        ]

        for i, (hero, class_name) in enumerate(party):
            if hero is None: continue

            # 슬롯 위치 계산
            x = self.start_x + (i * self.gap)
            y = self.start_y

            self.draw_slot(hero, class_name, x, y)

    def draw_slot(self, hero, class_name, x, y):

        # --- 1. UI 아이콘 그리기 ---
        if class_name in self.images:
            self.images[class_name].draw(x, y)

        # 텍스트와 바는 아이콘 오른쪽으로 배치
        info_x = x + 30
        info_y = y + 10

        # --- 2. 레벨 텍스트 ---
        if self.font:
            level_str = f"LV.{getattr(hero, 'level', 30)}"
            # 그림자
            self.font.draw(info_x + 1, info_y - 1, level_str, (0, 0, 0))
            # 본 글씨 (노랑)
            self.font.draw(info_x, info_y, level_str, (1, 0.9, 0.2))

        # --- 3. HP 바 설정 ---
        # HP 바 위치 (경험치 바가 없으므로 위치를 살짝 조정해도 좋지만, 기존 위치 유지)
        bar_x = x + 30
        bar_y = y + 10
        bar_w = 100
        bar_h = 10

        # 체력 비율 계산
        current_hp = hero.hp
        max_hp = hero.max_hp
        hp_ratio = current_hp / max_hp
        if hp_ratio < 0: hp_ratio = 0
        if hp_ratio > 1: hp_ratio = 1

        # --- 4. 선을 겹쳐서 두께 만들기 (요청하신 방식) ---

        # 바의 아래쪽부터 위쪽으로 한 줄씩 쌓아 올립니다.
        # bar_y가 위쪽 좌표이므로, 시작점은 (bar_y - bar_h) 입니다.
        bottom_y = bar_y - bar_h

        for i in range(bar_h):
            y_pos = bottom_y + i  # 한 줄씩 위로 올라감

            # (1) 배경선 (검정/회색 역할) - 전체 길이
            # 배경은 처음부터 끝(bar_w)까지 그립니다.
            draw_line(bar_x, y_pos, bar_x + bar_w, y_pos)

            # (2) 체력선 (빨강 역할) - 남은 체력만큼만
            # 체력이 있는 부분만 덮어 씌웁니다.
            current_w = bar_w * hp_ratio
            if current_w > 0:
                draw_rectangle(bar_x, y_pos, bar_x + current_w, y_pos)

        # (3) 외곽선 (깔끔하게 마무리)
        draw_rectangle(bar_x, bar_y - bar_h, bar_x + bar_w, bar_y)

        # --- 5. 체력 텍스트 그리기 ---
        if self.font:
            hp_str = f"{int(current_hp)}/{int(max_hp)}"

            # 텍스트 중앙 정렬 위치 계산
            text_x = bar_x + (bar_w // 2) - 30
            text_y = bar_y - (bar_h // 2)

            self.font.draw(text_x + 1, text_y - 1, hp_str, (0, 0, 0))  # 그림자
            self.font.draw(text_x, text_y, hp_str, (1, 1, 1))  # 흰색 글씨