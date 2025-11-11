import time
frame_time = 0.0

def change_mode(mode):
    pass

def push_mode(mode):
    pass

def pop_mode():
    pass

def quit():
    global running
    running = False



def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    while running:
        handle_events()

        update_world()  # 객체들의 상호작용을 시뮬레이션 , 계산
        render_world()  # 객체들의 모습을 그린다.
        delay(0.1)