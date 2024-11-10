import random
import time
from . import utils

def swap(cube, posisi1, posisi2):
    i1, j1, k1 = posisi1
    i2, j2, k2 = posisi2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

# Algoritma Steepest Ascent Hill Climbing
def steepest_ascent_algorithm(cube):
    N = len(cube)
    start_time = time.time()
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    costs = []
    
    # Generate all possible pairs once
    all_positions = [(i//(N*N), (i//N)%N, i%N) for i in range(N*N*N)]
    all_pairs = []
    for i in range(len(all_positions)):
        for j in range(i+1, len(all_positions)):
            all_pairs.append((all_positions[i], all_positions[j]))
    
    while True:
        found_improvement = False
        random.shuffle(all_pairs)  # Randomize pair order
        
        for pos1, pos2 in all_pairs:
            # Try swap
            swap(cube, pos1, pos2)
            new_cost = utils.objective_function(cube)
            
            if new_cost < best_cost:
                best_cost = new_cost
                costs.append(best_cost)
                found_improvement = True
                break  # Found better solution, try new random order
            else:
                swap(cube, pos1, pos2)  # Undo swap
        
        if not found_improvement:
            break  # No improvement found after checking all pairs
    
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "average_cost": round(best_cost/109, 4),
        "duration": round(duration, 2),
        "iteration": len(costs),
        "costs": costs
    }