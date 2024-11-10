import time
import math
import random
from typing import List, Tuple
from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> None:
    """Swaps elements in the cube at the given positions."""
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

def get_random_neighbor(N: int) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """Generates two distinct random positions in the cube."""
    pos1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    # Ensure the positions are not the same
    while pos1 == pos2:
        pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    return pos1, pos2

def acceptance_function(delta_cost: float, temperature: float) -> bool:
    """Determines if a worse solution should be accepted based on probability."""
    if delta_cost > 0:
        return True # Accept if the new solution is better
    else:
        r = random.random()
        # Accept with a probability based on temperature
        return r < math.exp(delta_cost / temperature)

def initialize_random_cube(N: int) -> List[List[List[int]]]:
    """Generates an N x N x N cube with random integers between 1 and 100."""
    return [[[random.randint(1, 100) for _ in range(N)] for _ in range(N)] for _ in range(N)]

def simulated_annealing_algorithm(cube: List[List[List[int]]], T_max: float = 100.0, T_min: float = 0.1, 
                                E_threshold: float = 0.01, cooling_rate: float = 0.9993,
                                max_no_improvement: int = 1000, max_iterations: int = 10000):
    """Performs the simulated annealing algorithm to optimize the cube configuration."""
    current_cost = utils.objective_function(cube) # Initial cost
    best_cost = current_cost # Set current cost as the best cost
    temperature = T_max # Set the temperature with maximum temperature
    iterations = 0
    no_improvement = 0
    local_optima = 0

    costs = []
    exps = []

    # Start the timer
    start_time = time.time()

    while temperature > T_min and current_cost > E_threshold and iterations < max_iterations:
        # Get random positions
        pos1, pos2 = get_random_neighbor(len(cube))
        # Swap
        swap_elements(cube, pos1, pos2)
        # Calculate the new cost
        new_cost = utils.objective_function(cube)
        delta_cost = current_cost - new_cost

        # Check if the new solution shoul be accepted
        if acceptance_function(delta_cost, temperature):
            if delta_cost < 0:
                local_optima += 1 # Count if worse solution is accepted
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                no_improvement = 0
            else:
                no_improvement += 1
        else:
            swap_elements(cube, pos1, pos2) # Revert swap if not accepted
            no_improvement += 1

        # Stop if reached no improvement limit
        if no_improvement >= max_no_improvement:
            break

        temperature *= cooling_rate # Decrease the temperature
        costs.append(current_cost)

        # Record acceptance probability every 200 iterations
        if iterations % 200 == 0:
            exp_delta_E_T = 1 if delta_cost > 0 else math.exp(delta_cost / temperature)
            exps.append(exp_delta_E_T)

        iterations += 1

    # Calculate the duration
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs),
        "local_optima": local_optima,
        "costs": costs,
        "exps": exps
    }