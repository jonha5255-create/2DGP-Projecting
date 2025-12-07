

world = [[] for _ in range(4)]


def add_object(o, depth = 0):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    global world

    for layer in world:
        layer.clear()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    print('삭제하려는 객체가 없어요')