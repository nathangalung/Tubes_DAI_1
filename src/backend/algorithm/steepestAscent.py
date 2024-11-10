import itertools
import time
import utils

def swap(cube, posisi1, posisi2):
    i1, j1, k1 = posisi1
    i2, j2, k2 = posisi2
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

# Algoritma Steepest Ascent Hill Climbing
def steepest_ascent(cube, N):
    start_time = time.time()
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    costs = [current_cost]
    
    while True:
        best_swap = None
        
        # Mencari anak terbaik
        for posisi1 in itertools.product(range(N), repeat=3):
            for posisi2 in itertools.product(range(N), repeat=3):
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
        "iterations": len(costs)
    }
