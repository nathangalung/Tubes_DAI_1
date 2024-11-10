import time
from typing import Tuple, List
from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int], calculate_cost: bool = False) -> int:
    """Swaps elements in the cube at the given positions pos1 and pos2."""
    i, j, k = pos1
    l, m, n = pos2
    cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

def find_best_neighbor(cube: List[List[List[int]]], best_cost: int, max_sideways: int, sideways: int) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
    """Finds the best neighboring configuration of the cube by trying all possible swaps."""
    N = len(cube)
    best_neighbor_cost = best_cost
    best_swap = (-1, -1, -1, -1, -1, -1)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(i, N):  
                    for m in (range(j, N) if i == l else range(N)):
                        for n in (range(k, N) if i == l and j == m else range(N)):
                            if (i == l and j == m and k == n):
                                continue 

                            swap_elements(cube, (i, j, k), (l, m, n))
                            new_cost = utils.objective_function(cube)

                            if new_cost < best_neighbor_cost or (new_cost == best_neighbor_cost and sideways < max_sideways):
                                best_neighbor_cost = new_cost 
                                best_swap = (i, j, k, l, m, n) 

                            swap_elements(cube, (i, j, k), (l, m, n))

    return best_neighbor_cost, best_swap

def sideways_move_algorithm(cube: List[List[List[int]]], max_sideways: int = 30) -> dict:
    """Performs the sideways move algorithm to optimize the cube configuration."""
    current_cost = utils.objective_function(cube)
    best_cost = current_cost 
    iterations, sideways = 0, 0 
    costs = []  

    start_time = time.time() 

    while True:
        best_neighbor_cost, best_swap = find_best_neighbor(cube, best_cost, max_sideways, sideways)

        if sideways >= max_sideways:
            break

        if best_swap != (-1, -1, -1, -1, -1, -1):
            i, j, k, l, m, n = best_swap
            swap_elements(cube, (i, j, k), (l, m, n)) 

            current_cost = best_neighbor_cost

            if current_cost < best_cost:
                best_cost = current_cost 
                sideways = 0 
            elif current_cost == best_cost:
                sideways += 1

        iterations += 1
        costs.append(best_cost)

    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2), 
        "iterations": iterations, 
        "costs": costs 
    }