import random
import time
from . import utils

def swap_two_random_positions(cube):
    # Mengacak dua posisi dalam kubus dan menukarnya
    N = len(cube)
    pos1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    return cube

def random_restart_algorithm(cube):
    N = len(cube)
    start_time = time.time()
    max_restarts = 10
    max_iterations = 1000
    best_cube = None
    best_cost = 0
    restarts = 0
    costs = []

    for restart in range(max_restarts):
        restart += 1
        cube = utils.initialize_random_cube(N)
        initial_state = cube.copy()
        current_cost = utils.objective_function(cube)
        costs_restart = {}
        costs_restart[f"costs_restart_{restart+1}"] = []
        
        for iteration in range(max_iterations):
            new_cube = swap_two_random_positions(cube.copy())
            new_cost = utils.objective_function(new_cube)
            
            if new_cost < current_cost:
                cube = new_cube
                current_cost = new_cost
            
            # Simpan solusi terbaik jika ditemukan
            if current_cost < best_cost:
                best_cube = cube.copy()
                best_cost = current_cost
                costs_restart[f"costs_restart_{restart+1}"].append(best_cost)
            
            # Jika solusi sempurna (fitness cost = 0) ditemukan
            if current_cost == 0:
                break
        
        costs.extend(costs_restart[f"costs_restart_{restart+1}"])
        
        # Jika solusi ditemukan
        if current_cost == 0:
            break

    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs) + 1,
        "costs": costs
    }
