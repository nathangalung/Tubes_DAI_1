import random
import time
from . import utils

def swap_two_random_positions(cube):
    N = len(cube)
    posisi1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    posisi2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
    cube[posisi1], cube[posisi2] = cube[posisi2], cube[posisi1]
    return cube

def random_restart_algorithm(cube, max_restarts=10, max_iterations_per_restart=1000):
    N = len(cube)
    start_time = time.time()
    best_cube = None
    best_cost = float('inf')  
    costs_history = {}
    total_iterations = 0

    for restart in range(max_restarts):
        current_cube = utils.initialize_random_cube(N)
        current_cost = utils.objective_function(current_cube)
        costs_history[f"restart_{restart+1}"] = {
            "costs": [],
            "iterations": 0
        }
        
        
        iterations_this_restart = 0
        while iterations_this_restart < max_iterations_per_restart:
            new_cube = swap_two_random_positions(current_cube.copy())
            new_cost = utils.objective_function(new_cube)
            
            if new_cost < current_cost:
                current_cube = new_cube
                current_cost = new_cost
                costs_history[f"restart_{restart+1}"]["costs"].append(current_cost)
            
            if current_cost < best_cost:
                best_cube = current_cube.copy()
                best_cost = current_cost
            
            iterations_this_restart += 1
            total_iterations += 1
            costs_history[f"restart_{restart+1}"]["iterations"] = iterations_this_restart
            
            if current_cost == 0: 
                break
        
        if current_cost == 0:
            break

    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs_history) + 1,
        "costs": costs_history,
        "restart": restart
    }
