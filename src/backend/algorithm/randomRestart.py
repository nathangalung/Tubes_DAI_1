import time
import random
from . import utils

def generate_random_neighbor(cube):
    N = len(cube)
    i1, j1, k1 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    while i1 == i2 and j1 == j2 and k1 == k2:
        i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    
    new_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    # menukar elemen
    new_cube[i1][j1][k1], new_cube[i2][j2][k2] = new_cube[i2][j2][k2], new_cube[i1][j1][k1]
    return new_cube

def random_restart_algorithm(cube, max_iterations_per_restart=1000, max_restart=10):
    N = len(cube)
    # Inisialisasi current cube dan current cost
    current_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    current_cost = utils.objective_function(current_cube)
    
    best_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    best_cost = current_cost
    restart = 0
    costs = []
    
    start_time = time.time()

    # Restart loop
    while restart < max_restart:
        iteration = 0
        iteration_restart = []

        # Iterasi dalam range max iterations per restart
        while iteration < max_iterations_per_restart:
            # Generate neighbor random dan hitung costnya
            neighbor_cube = generate_random_neighbor(current_cube)
            neighbor_cost = utils.objective_function(neighbor_cube)

            # kalau neighbor lebih baik, update current cube dan cost
            if neighbor_cost < current_cost:
                current_cube = neighbor_cube
                current_cost = neighbor_cost

                # Perbarui solusi terbaik jika neighbor lebih baik dari solusi terbaik
                if current_cost < best_cost:
                    best_cube = current_cube
                    best_cost = current_cost
            iteration += 1
            costs.append(best_cost)

        # Setelah maksimal iterasi per restart, restart dengan random cube
        current_cube = utils.initialize_random_cube(N)
        current_cost = utils.objective_function(current_cube)
        restart += 1  # counter restart
        iteration_restart.append(iteration)

    duration = time.time() - start_time

    return {
        "final_cube": best_cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs),
        "iteration_restart": iteration_restart,
        "restart": restart,
        "costs": costs
    }