import random
import time
from . import utils

def swap(cube, posisi1, posisi2):
    i1, j1, k1 = posisi1
    i2, j2, k2 = posisi2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

# Algoritma Steepest Ascent Hill Climbing
def steepest_ascent_algorithm(cube, max_iterations=10000):
    N = len(cube)
    start_time = time.time()
    current_cost = utils.objective_function(cube)
    costs = [current_cost]
    iterations = 0
    
    while (iterations < max_iterations):
        best_cost = current_cost
        best_swap = None
        iterations += 1
        
        # Mencari anak terbaik
        for _ in range(100):
            posisi1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
            posisi2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
            
            if posisi1 == posisi2:
                continue

            swap(cube, posisi1, posisi2)
            new_cost = utils.objective_function(cube)
            
            if new_cost < best_cost:
                best_cost = new_cost
                best_swap = (posisi1, posisi2)
            
            swap(cube, posisi1, posisi2)
        
        if best_swap:
            swap(cube, best_swap[0], best_swap[1])
            current_cost = best_cost
            costs.append(current_cost)
        else:
            break 
    
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs),
        "costs": costs
    }
