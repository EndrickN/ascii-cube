import sys
import time
import math


WIDTH = 40
HEIGHT = 40

center_x = WIDTH // 2
center_y = HEIGHT // 2

VERTICES = [
    (-3, -3, -3),
    (-3, -3, +3),
    (-3, +3, -3),
    (-3, +3, +3),
    (+3, -3, -3),
    (+3, -3, +3),
    (+3, +3, -3),
    (+3, +3, +3)
]

EDGES = []
for i in range(len(VERTICES)):
    for j in range(i + 1, len(VERTICES)):
        v1 = VERTICES[i]
        v2 = VERTICES[j]
        diff = sum(a != b for a, b in zip(v1, v2))
        if diff == 1: EDGES.append((i, j))

FOCAL_LENGTH = 30
CAMERA_DIST = 12

angle = 0.5
angle2 = 0.3


def rotate(x, y, z, angle, angle2):
    old_x = x
    old_z = z
    x = old_x*math.cos(angle) - old_z*math.sin(angle)
    z = old_x*math.sin(angle) + old_z*math.cos(angle)

    old_y = y
    old_z = z
    y = old_y*math.cos(angle2) - old_z*math.sin(angle2)
    z = old_y*math.sin(angle2) + old_z*math.cos(angle2)

    return x, y, z

def project(x, y, z):
    depth = z + CAMERA_DIST
    if depth < 0.1: return None
    sx = round(center_x + x*FOCAL_LENGTH / depth)
    sy = round(center_y + y*FOCAL_LENGTH / depth)

    return sx, sy

def plot(screen, x, y):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        screen[y][x] = '#'

def draw_line(screen, a, b):
    if a is None or b is None: 
        return

    x1, y1 = a
    x2, y2 = b

    steps = max(abs(x2 - x1), abs(y2 - y1)) 

    if steps == 0:
        plot(screen, x1, y1)
        return

    for i in range(steps + 1):
        t = i / steps
        x = round(x1 + (x2 - x1) * t)
        y = round(y1 + (y2 - y1) * t)
        plot(screen, x, y)

sys.stdout.write("\033[2J\033[H")
sys.stdout.flush()
while True:
    screen = [['.']*WIDTH for _ in range(HEIGHT)]

    projected = []
    for v in VERTICES:
        r = rotate(v[0], v[1], v[2], angle, angle2)
        p = project(r[0], r[1], r[2])
        projected.append(p)

    for i, j in EDGES:
        draw_line(screen, projected[i], projected[j])

    frame = "\n".join(" ".join(row) for row in screen)

    angle += 0.05
    angle2 += 0.03

    sys.stdout.write("\033[H" + frame)
    sys.stdout.flush()
    time.sleep(0.2)
    