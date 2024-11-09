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

def stochastic_algorithm(cube: List[List[List[int]]]) -> Tuple[List[List[List[int]]], float, List[float], float]:
    """
    Performs stochastic hill climbing with a fixed number of iterations.
    """
    N = len(cube)
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    max_iterations = 1000
    iterations = 0
    costs = []

    start_time = time.time()

    while iterations < max_iterations:
        # Generate two random positions
        pos1 = (select_random_position(N), select_random_position(N), select_random_position(N))
        pos2 = (select_random_position(N), select_random_position(N), select_random_position(N))
        
        while pos1 == pos2:
            pos2 = (select_random_position(N), select_random_position(N), select_random_position(N))

        cost_change = calculate_cost_change(cube, pos1, pos2)

        if cost_change < 0:
            i1, j1, k1 = pos1
            i2, j2, k2 = pos2
            cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]
            current_cost += cost_change
            best_cost = current_cost

        costs.append(current_cost)
        iterations += 1

    duration = time.time() - start_time
    # print(f"Stochastic Hill Climbing: iterations={iterations}, Time={duration:.2f} seconds, Final Cost={current_cost}")

    # utils.save_json(costs, "stochastic_costs.json")
    # utils.plot_function("stochastic_costs.json", "stochastic_objective_function_plot.png", 
    #                    "Iteration", "Objective Function", "Stochastic Algorithm Plot")
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs) + 1,
        "costs": costs
    }