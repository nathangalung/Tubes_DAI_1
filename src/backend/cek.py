import time
import random
from typing import List
from algorithm import utils

def generate_random_neighbor(cube):
    N = len(cube)
    i1, j1, k1 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    while i1 == i2 and j1 == j2 and k1 == k2:
        i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    
    # Create deep copy using list comprehension
    new_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    # Swap elements to create a new neighbor
    new_cube[i1][j1][k1], new_cube[i2][j2][k2] = new_cube[i2][j2][k2], new_cube[i1][j1][k1]
    return new_cube

def random_restart_algorithm(cube, max_iterations_per_restart=1000, max_restart=10):
    N = len(cube)
    # Initialize the current and best cubes with the input cube
    current_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    current_cost = utils.objective_function(current_cube)
    
    # Set the initial best solution to the starting cube
    best_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    best_cost = current_cost
    restart = 0
    costs = []  # Track cost at each iteration
    iteration_restart = []
    
    start_time = time.time()

    # Restart loop
    while restart < max_restart:
        iteration = 0

        # Iterations within each restart
        while iteration < max_iterations_per_restart:
            # Generate a random neighbor and calculate its cost
            neighbor_cube = generate_random_neighbor(current_cube)
            neighbor_cost = utils.objective_function(neighbor_cube)

            # If the neighbor is better, update current cube and cost
            if neighbor_cost < current_cost:
                current_cube = neighbor_cube
                current_cost = neighbor_cost

                # Update best solution if the neighbor is better than the global best
                if current_cost < best_cost:
                    best_cube = current_cube
                    best_cost = current_cost
            iteration += 1
            costs.append(best_cost)

        # After max_iterations_per_restart, restart with a new random cube
        current_cube = utils.initialize_random_cube(N)
        current_cost = utils.objective_function(current_cube)
        restart += 1
        iteration_restart.append(iteration)

    duration = time.time() - start_time
    
    print(f"Iteration per Restart: {iteration_restart}")
    print(f"Best cost: {best_cost}")
    print(f"Duration: {duration}")

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

cube = initialize_random_cube(5)

random_restart_algorithm(cube)

