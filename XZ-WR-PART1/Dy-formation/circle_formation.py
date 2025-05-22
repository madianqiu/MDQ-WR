import numpy as np

def generate_circle_formation():
    N = 25
    R = 5.0
    leader_pos = (0, 0)
    leader_x, leader_y = leader_pos
    positions = [leader_pos]

    delta_theta = 2 * np.pi / (N - 1)
    for i in range(1, N):
        theta = delta_theta * i
        R_i = R + np.random.uniform(-0.5, 0.5)
        x = leader_x + R_i * np.cos(theta)
        y = leader_y + R_i * np.sin(theta)
        positions.append((x, y))

    return positions