import pygame as pg
from random import random
from collections import deque


def draw_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and grid[y][x] != 1 else False
    ways = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def right_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('brown'), draw_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[2] and grid[grid_y][grid_x] != 1 else False


def left_click_mouse_start():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def bfs(start, goal, graph):
    queue = deque([start])
    visited = {}


    while queue:
        cur_node = queue.popleft()

        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node

    current = goal
    path = [current]

    while current != start:
     current = visited[current]
     path.append(current)

    path.reverse()

    return path


def move(X, Y, speed, path, i):
    distance = pg.math.Vector2(path[i]) - (X, Y)

    if distance.length() < speed:
        X, Y = path[i]
        i = (i + 1) % len(path)

        if  (X, Y) == path[-1]:
            path.clear()

    else:

        distance.scale_to_length(speed)

        new_pos = pg.math.Vector2(X, Y) + distance
        X, Y = (new_pos.x, new_pos.y)

    return X, Y, i





# drawing grid
cols, rows = 25, 15
TILE = 60
sc = pg.display.set_mode([cols * TILE, rows * TILE])


# dict of adjacency lists
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
print(grid)
graph = {}

for y, row in enumerate(grid):
    for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


# draw_path_start-variables
start = ()
path = ()

# Move-variables
X = 0
Y = 0
speed = 4
next_pos_index = 1



pg.init()
clock = pg.time.Clock()


while True:
    sc.fill("black")

    for y, row in enumerate(grid):
        for x, col in enumerate(row):
         if col:
            pg.draw.rect(sc, pg.Color('forestgreen'), draw_rect(x, y))


    pg.draw.rect(sc, "darkorange", (X, Y, 60, 60))


    if left_click_mouse_start():
        start = left_click_mouse_start()


    if right_click_mouse_pos():
        path = bfs(start, right_click_mouse_pos(), graph)
        path = [(x * TILE, y * TILE) for x, y in path]


    if path:
        X, Y, next_pos_index = move(X, Y, speed, path, next_pos_index)


















    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)
