import numpy as np

def generate_line_formation():
    N = 25
    dx_min = 1.0
    rx = 0.5
    leader_pos = (0, 0)
    leader_x, leader_y = leader_pos
    positions = [leader_pos]

    for i in range(1, N):
        rand_dx = np.random.uniform(0, rx)
        x = leader_x + (dx_min + rand_dx) * (i - N / 2)
        y = leader_y
        positions.append((x, y))

    return positions