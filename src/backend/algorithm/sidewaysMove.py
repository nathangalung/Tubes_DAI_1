import time
import random
from typing import Tuple, List
from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> None:
    """Swaps elements in the cube at the given positions."""
    i, j, k = pos1
    l, m, n = pos2
    cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

def find_best_neighbor(cube: List[List[List[int]]], N: int, all_pairs: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]], 
                      best_cost: int, max_sideways: int, sideways: int) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
    """Finds best neighbor using random pair selection."""
    best_neighbor_cost = best_cost
    best_swap = (-1, -1, -1, -1, -1, -1)
    
    # Shuffle pairs for random search
    random.shuffle(all_pairs)
    
    for pos1, pos2 in all_pairs:
        swap_elements(cube, pos1, pos2)
        new_cost = utils.objective_function(cube)
        
        if new_cost < best_neighbor_cost or (new_cost == best_neighbor_cost and sideways < max_sideways):
            best_neighbor_cost = new_cost
            i, j, k = pos1
            l, m, n = pos2
            best_swap = (i, j, k, l, m, n)
            
        swap_elements(cube, pos1, pos2)
        
        if new_cost < best_neighbor_cost:
            break  # Found improvement, no need to check more pairs
            
    return best_neighbor_cost, best_swap

def sideways_move_algorithm(cube: List[List[List[int]]], max_sideways: int = 30) -> dict:
    """Performs sideways move hill climbing with random neighbor selection."""
    N = len(cube)
    start_time = time.time()
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    costs = [current_cost]
    iterations = 0
    sideways = 0
    
    # Generate all possible pairs once
    all_positions = [(i//(N*N), (i//N)%N, i%N) for i in range(N*N*N)]
    all_pairs = []
    for i in range(len(all_positions)):
        for j in range(i+1, len(all_positions)):
            all_pairs.append((all_positions[i], all_positions[j]))
    
    while True:
        best_neighbor_cost, best_swap = find_best_neighbor(cube, N, all_pairs, best_cost, max_sideways, sideways)
        
        if best_swap == (-1, -1, -1, -1, -1, -1):
            break
            
        i, j, k, l, m, n = best_swap
        swap_elements(cube, (i, j, k), (l, m, n))
        
        if best_neighbor_cost < best_cost:
            best_cost = best_neighbor_cost
            sideways = 0
        elif best_neighbor_cost == best_cost:
            sideways += 1
            if sideways >= max_sideways:
                break
                
        costs.append(best_cost)
        iterations += 1
    
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": iterations,
        "costs": costs
    }