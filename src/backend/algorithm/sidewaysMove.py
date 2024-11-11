import copy
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
    best_swap = (-1, -1, -1, -1, -1, -1) #Default for invalid swap
    
    # Shuffle pairs for random search
    random.shuffle(all_pairs)
    
    for pos1, pos2 in all_pairs:
        # Swap elements and check cost
        swap_elements(cube, pos1, pos2)
        new_cost = utils.objective_function(cube)
        
        # Update if new cost is better or sideways move allowed
        if new_cost < best_neighbor_cost or (new_cost == best_neighbor_cost and sideways < max_sideways):
            best_neighbor_cost = new_cost
            i, j, k = pos1
            l, m, n = pos2
            best_swap = (i, j, k, l, m, n)

        # Revert the swap    
        swap_elements(cube, pos1, pos2)
        
        # Break if improvement found
        if new_cost < best_neighbor_cost:
            break
            
    return best_neighbor_cost, best_swap

def sideways_move_algorithm(cube: List[List[List[int]]], max_sideways: int = 10) -> dict:
    """Executes a hill climbing approach that allows sideways moves and uses random selection for neighbors."""
    N = len(cube)
    current_cost = utils.objective_function(cube) 
    best_cost = current_cost
    costs = []
    states = []
    iteration = 0
    sideways = 0

    # Start the timer
    start_time = time.time()
    
    # Generate all possible pairs of positions in the cube
    all_positions = [(i//(N*N), (i//N)%N, i%N) for i in range(N*N*N)]
    all_pairs = []
    for i in range(len(all_positions)):
        for j in range(i+1, len(all_positions)):
            all_pairs.append((all_positions[i], all_positions[j]))
    
    while True:
        # Get the best neighbor
        best_neighbor_cost, best_swap = find_best_neighbor(cube, N, all_pairs, best_cost, max_sideways, sideways)
        
        # Stop if no better neighbor found
        if best_swap == (-1, -1, -1, -1, -1, -1):
            break

        # Perform the best swap    
        i, j, k, l, m, n = best_swap
        swap_elements(cube, (i, j, k), (l, m, n))
        
        # Update cost and check sideways moves
        if best_neighbor_cost < best_cost:
            best_cost = best_neighbor_cost
            sideways = 0
        elif best_neighbor_cost == best_cost:
            sideways += 1
            if sideways >= max_sideways:
                break
                
        costs.append(best_cost)
        states.append(copy.deepcopy(cube))
        iteration += 1
    
    # Calculate total duration
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "average_cost": round(best_cost/109, 4),
        "duration": round(duration, 2),
        "iteration": len(costs),
        "costs": costs,
        "states": states
    }