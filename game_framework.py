import time
frame_time = 0.0

running = None
stack = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if(len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if(len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    if(len(stack) > 0):
        stack[-1].resume()

def quit():
    global running
    running = False



def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()  # 객체들의 상호작용을 시뮬레이션 , 계산
        stack[-1].draw()  # 객체들의 모습을 그린다.
        frame_time = time.time() - current_time
        frame_time = 1.0/frame_time
        current_time += frame_time

    while(len(stack) > 0):
        stack[-1].finish()
        stack.pop()