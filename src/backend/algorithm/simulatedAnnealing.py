import time
import math
import random
from typing import List, Tuple

from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> None:
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

def get_random_neighbor(N: int) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    pos1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    while pos1 == pos2:
        pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    return pos1, pos2

def acceptance_function(delta_cost: float, temperature: float) -> bool:
    if delta_cost > 0:
        return True
    else:
        r = random.random()
        return r < math.exp(delta_cost / temperature)

def simulated_annealing_algorithm(cube: List[List[List[int]]], T_max: float = 100.0, T_min: float = 0.1, 
                                E_threshold: float = 0.01, cooling_rate: float = 0.9993,
                                max_no_improvement: int = 1000, max_iterations: int = 10000):
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    temperature = T_max
    iterations = 0
    no_improvement = 0
    local_optima = 0

    costs = []
    exps = []

    start_time = time.time()

    while temperature > T_min and current_cost > E_threshold and iterations < max_iterations:
        pos1, pos2 = get_random_neighbor(len(cube))
        swap_elements(cube, pos1, pos2)

        new_cost = utils.objective_function(cube)
        delta_cost = current_cost - new_cost

        if acceptance_function(delta_cost, temperature):
            if delta_cost > 0:
                local_optima += 1
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                no_improvement = 0
            else:
                no_improvement += 1
        else:
            swap_elements(cube, pos1, pos2)
            no_improvement += 1

        if no_improvement >= max_no_improvement:
            break

        temperature *= cooling_rate
        costs.append(current_cost)

        if iterations % 200 == 0:
            exp_delta_E_T = 1 if delta_cost > 0 else math.exp(delta_cost / temperature)
            exps.append(exp_delta_E_T)

        iterations += 1

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