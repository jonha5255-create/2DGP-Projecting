


def handle_events():
    global running, Warrior

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            Warrior.handle_event(event)


def reset_world():
    global Warrior


    Warrior = warrior()
    game_world.add_object(Warrior)

    Boss = boss()
    game_world.add_object(Boss)

    Enemy = enemy()
    game_world.add_object(Enemy)




def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()
