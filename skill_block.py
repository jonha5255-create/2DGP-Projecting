from pico2d import *

class SKILLBLOCK:
    BLOCK_WIDTH = 125
    BLOCK_HEIGHT = 90

    JOB_SKILL = {
        'warrior' : 'warrior_skill.png',
        'archer' : 'archer_skill.png',
        'healer' : 'healer_skill.png'
    }
    def __init__(self):
        random_job = random.choice(['warrior', 'archer', 'healer'])
        self.skill_type = random_job

        image_file = self.JOB_SKILL.get(skill_type, '.png')
        self.x, self.y = 700, 90

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass