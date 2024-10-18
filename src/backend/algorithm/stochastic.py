import numpy as np
import time
import math
import random

def objective_function(cube):
    """
    Calculate the objective function cost based on the deviation from the magic number.
    Args:
    - cube (numpy array): The 3D cube configuration.
    Returns:
    - cost (int): The total deviation from the magic number across all rows, columns, and diagonals.
    """
    N = cube.shape[0]
    magic_number = (N * (N**3 + 1)) // 2
    cost = 0

    # Row, column, and pillar sums
    for i in range(N):
        for j in range(N):
            row_sum = np.sum(cube[i, j, :])  # Row
            col_sum = np.sum(cube[i, :, j])  # Column
            pillar_sum = np.sum(cube[:, i, j])  # Pillar
            cost += abs(magic_number - row_sum)
            cost += abs(magic_number - col_sum)
            cost += abs(magic_number - pillar_sum)

    # Space diagonals (3D diagonals)
    diag1 = np.sum([cube[i, i, i] for i in range(N)])  # (0,0,0) to (N-1,N-1,N-1)
    diag2 = np.sum([cube[i, i, N - i - 1] for i in range(N)])  # (0,0,N-1) to (N-1,N-1,0)
    diag3 = np.sum([cube[i, N - i - 1, i] for i in range(N)])  # (0,N-1,0) to (N-1,0,N-1)
    diag4 = np.sum([cube[N - i - 1, i, i] for i in range(N)])  # (N-1,0,0) to (0,N-1,N-1)

    cost += abs(magic_number - diag1)
    cost += abs(magic_number - diag2)
    cost += abs(magic_number - diag3)
    cost += abs(magic_number - diag4)

    return cost

def select_random_position(N):
    """
    Selects a random position in the cube.
    Args:
    - N (int): Size of the cube.
    Returns:
    - int: A random position between 0 and N-1.
    """
    return random.randint(0, N-1)

def generate_random_neighbor(cube):
    N = cube.shape[0]
    i1, j1, k1 = select_random_position(N), select_random_position(N), select_random_position(N)
    i2, j2, k2 = select_random_position(N), select_random_position(N), select_random_position(N)
    while i1 == i2 and j1 == j2 and k1 == k2:
        i2, j2, k2 = select_random_position(N), select_random_position(N), select_random_position(N)
    
    new_cube = np.copy(cube)
    new_cube[i1, j1, k1], new_cube[i2, j2, k2] = new_cube[i2, j2, k2], new_cube[i1, j1, k1]
    return new_cube

def stochastic_hill_climbing(cube, max_moves=1000, no_improvement_limit=100, min_improvement_threshold=5, exploration_prob=0.1):
    N = cube.shape[0]
    current_cube = np.copy(cube)
    current_cost = objective_function(current_cube)
    best_cube = np.copy(current_cube)
    best_cost = current_cost
    moves = 0
    no_improvement = 0

    start_time = time.time()

    while moves < max_moves and no_improvement < no_improvement_limit:
        # Generate a random neighbor
        neighbor_cube = generate_random_neighbor(current_cube)
        neighbor_cost = objective_function(neighbor_cube)

        # Decide whether to accept the neighbor
        if neighbor_cost < current_cost or random.random() < exploration_prob * math.exp(-(neighbor_cost - current_cost)):
            current_cube = neighbor_cube
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_cube = np.copy(current_cube)
                best_cost = current_cost
                no_improvement = 0
            else:
                no_improvement += 1
        else:
            no_improvement += 1

        # Adjust exploration probability occasionally
        if no_improvement % min_improvement_threshold == 0:
            exploration_prob = max(0.01, exploration_prob * 0.9)  # Reduce exploration probability

        moves += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Stochastic Hill Climbing: Moves={moves}, Time={elapsed_time:.2f} seconds, Best Cost={best_cost}")
    return best_cube, best_cost