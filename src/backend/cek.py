import time
import random
from typing import List
from algorithm import utils

def initialize_random_cube(N: int) -> List[List[List[int]]]:
    """
    Initializes a 3D cube of size N x N x N with unique random integers.
    """
    cube = [[[0 for _ in range(N)] for _ in range(N)] for _ in range(N)]
    used = set()

    for i in range(N):
        for j in range(N):
            for k in range(N):
                num = random.randint(1, N * N * N)
                while num in used:
                    num = random.randint(1, N * N * N)
                cube[i][j][k] = num
                used.add(num)

    return cube

def generate_random_neighbor(cube):
    N = len(cube)
    i1, j1, k1 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    while i1 == i2 and j1 == j2 and k1 == k2:
        i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    
    # Create deep copy using list comprehension
    new_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    # Fix indexing
    new_cube[i1][j1][k1], new_cube[i2][j2][k2] = new_cube[i2][j2][k2], new_cube[i1][j1][k1]
    return new_cube

def random_restart_algorithm(cube, max_iterations_per_restart=1000, max_restart=10):
    N = len(cube)
    current_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    current_cost = utils.objective_function(current_cube)
    best_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    best_cost = current_cost
    iteration = 0
    restart = 0
    
    start_time = time.time()
    costs = []
    iteration_restart = []  # Initialize empty list

    while restart < max_restart:
        neighbor_cube = generate_random_neighbor(current_cube)
        neighbor_cost = utils.objective_function(neighbor_cube)

        if neighbor_cost < best_cost:
            best_cube = [[[neighbor_cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
            best_cost = neighbor_cost
            iteration += 1
            print("Iteration:", iteration)
        else:
            current_cube = utils.initialize_random_cube(N)
            current_cost = utils.objective_function(current_cube)
            best_cube = [[[current_cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
            best_cost = current_cost
            restart += 1
            iteration = 0
        
        costs.append(best_cost)

        if iteration >= max_iterations_per_restart:
            iteration_restart.append(iteration)
            print("Restart ke:", restart)
            break

    # Ensure iteration_restart has at least one value
    if not iteration_restart and iteration > 0:
        iteration_restart.append(iteration)
    
    duration = time.time() - start_time
    
    print("Best cost: ", best_cost)
    print("Total Restart:", restart)

cube = initialize_random_cube(5)

random_restart_algorithm(cube)

