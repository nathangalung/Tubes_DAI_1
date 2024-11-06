import numpy as np
import time
from . import utils

def random_restart_hill_climbing(cube):
    N = cube.shape[0]
    best_cost = utils.objective_function(cube)
    total_moves = 0
    MAX_RESTARTS = 50
    MAX_MOVES_PER_RESTART = 1000
    start_time = time.time()

    for restart in range(MAX_RESTARTS):
        utils.initialize_random_cube(cube)  # Inisialisasi dengan kondisi acak
        cost = utils.objective_function(cube)
        moves = 0
        no_improvement_steps = 0
        MAX_NO_IMPROVEMENT_STEPS = 100

        while moves < MAX_MOVES_PER_RESTART and no_improvement_steps < MAX_NO_IMPROVEMENT_STEPS:
            best_neighbor_cost = cost
            swap_i, swap_j, swap_k, swap_l, swap_m, swap_n = -1, -1, -1, -1, -1, -1

            for i in range(N):
                for j in range(N):
                    for k in range(N):
                        for l in range(N):
                            for m in range(N):
                                for n in range(N):
                                    if i == l and j == m and k == n:
                                        continue

                                    # Melakukan swap
                                    cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]
                                    current_cost = utils.objective_function(cube)

                                    if current_cost < best_neighbor_cost:
                                        best_neighbor_cost = current_cost
                                        swap_i, swap_j, swap_k, swap_l, swap_m, swap_n = i, j, k, l, m, n

                                    # Batalkan swap
                                    cube[l][m][n], cube[i][j][k] = cube[i][j][k], cube[l][m][n]

            if best_neighbor_cost >= cost:
                no_improvement_steps += 1
            else:
                no_improvement_steps = 0

            if swap_i != -1:
                cube[swap_i][swap_j][swap_k], cube[swap_l][swap_m][swap_n] = cube[swap_l][swap_m][swap_n], cube[swap_i][swap_j][swap_k]
                cost = best_neighbor_cost

            moves += 1

        total_moves += moves
        best_cost = min(best_cost, cost)

    end_time = time.time()
    print(f"Random Restart Hill Climbing: Total Moves={total_moves}, Time={end_time - start_time:.2f} seconds, Best Cost={best_cost}")
    return cube
