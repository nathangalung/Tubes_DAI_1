import time
import random
from typing import List, Tuple
from . import utils

def select_random_position(N: int) -> int:
    """Selects a random position in the cube."""
    return random.randint(0, N - 1)

def calculate_cost_change(cube: List[List[List[int]]], 
                         pos1: Tuple[int, int, int], 
                         pos2: Tuple[int, int, int]) -> int:
    """
    Calculates the change in cost for a single swap between two positions.
    """
    original_cost = utils.objective_function(cube)
    # Perform the swap
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
    # Calculate the new cost after the swap
    new_cost = utils.objective_function(cube)
    # Undo the swap
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
    return new_cost - original_cost

def stochastic_algorithm(cube: List[List[List[int]]]) -> dict:
    N = len(cube)
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    costs = []
    max_iterations = 10000
    iterations = 0

    start_time = time.time()

    while iterations < max_iterations:
        # Generate single integer indices instead of tuples
        i1, j1, k1 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
        i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
        
        # Ensure different positions
        while (i1, j1, k1) == (i2, j2, k2):
            i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)

        # Calculate cost change directly
        original_cost = utils.objective_function(cube)
        
        # Perform swap
        cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
        new_cost = utils.objective_function(cube)
        cost_change = new_cost - original_cost

        if cost_change < 0:
            current_cost = new_cost
            best_cost = min(best_cost, current_cost)
        else:
            # Undo swap if no improvement
            cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

        costs.append(current_cost)
        iterations += 1

    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs),
        "costs": costs
    }