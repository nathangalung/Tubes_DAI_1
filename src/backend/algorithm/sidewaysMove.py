import time
from typing import Tuple, List
from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int], calculate_cost: bool = False) -> int:
    i, j, k = pos1
    l, m, n = pos2
    cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

    if calculate_cost:
        cost = utils.objective_function(cube)
        cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]
        return cost

    return None

def find_best_neighbor(cube: List[List[List[int]]], best_cost: int, max_sideways: int, sideways: int) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
    N = len(cube)
    best_neighbor_cost = best_cost
    best_swap = (-1, -1, -1, -1, -1, -1)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                current_cost = utils.objective_function(cube)
                
                for l in range(i, N):  
                    for m in (range(j, N) if i == l else range(N)):
                        for n in (range(k, N) if i == l and j == m else range(N)):
                            if (i == l and j == m and k == n):
                                continue
                            
                            swap_elements(cube, (i, j, k), (l, m, n))
                            new_cost = utils.objective_function(cube) + utils.objective_function(cube)
                            total_cost = best_cost - current_cost + new_cost

                            if total_cost < best_neighbor_cost or (
                                total_cost == best_neighbor_cost and sideways < max_sideways
                            ):
                                best_neighbor_cost = total_cost
                                best_swap = (i, j, k, l, m, n)

                            swap_elements(cube, (i, j, k), (l, m, n))

    return best_neighbor_cost, best_swap

def sideways_move_algorithm(cube: List[List[List[int]]], max_sideways: int = 100, max_iterations: int = 1000) -> Tuple[List[List[List[int]]], int, List[int], float]:
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    iterations, sideways = 0, 0
    costs = []

    start_time = time.time()

    while iterations < max_iterations:
        best_neighbor_cost, best_swap = find_best_neighbor(cube, best_cost, max_sideways, sideways)

        if best_neighbor_cost >= best_cost and sideways >= max_sideways:
            break

        if best_neighbor_cost == best_cost:
            sideways += 1
        else:
            sideways = 0

        if best_swap != (-1, -1, -1, -1, -1, -1):
            i, j, k, l, m, n = best_swap
            swap_elements(cube, (i, j, k), (l, m, n))
            best_cost = best_neighbor_cost

        iterations += 1
        costs.append(current_cost)

    duration = time.time() - start_time

    utils.save_json(costs, "sideways_costs.json")
    # utils.plot_function("sideways_costs.json", "sideways_objective_function_plot.png", "Iteration",
    #                     "Objective Function Cost", "Objective Function Cost per Iteration")

    return cube, best_cost, costs, f"{duration:.2f}"