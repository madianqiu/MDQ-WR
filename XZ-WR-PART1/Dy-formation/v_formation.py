import numpy as np

def generate_v_formation():
    N = 25
    dx_min, dy_min = 0.5, 1.5
    rx, ry = 0.2, 0.2
    leader_pos = (0, 0)
    leader_x, leader_y = leader_pos
    positions = [leader_pos]

    for i in range(1, N):
        rand_dx, rand_dy = np.random.uniform(0, rx), np.random.uniform(0, ry)
        x = leader_x + (dx_min + rand_dx) * (i - N / 2)
        y = leader_y - (dy_min + rand_dy) * abs(i - N / 2)
        positions.append((x, y))

    return positions