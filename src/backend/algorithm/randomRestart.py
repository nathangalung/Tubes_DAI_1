import copy
import time
import random
from typing import List, Tuple
from . import utils

def swap_elements(cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> None:
    #menukar elemen 
    i, j, k = pos1
    l, m, n = pos2
    cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

def generate_random_neighbor(cube: List[List[List[int]]]) -> List[List[List[int]]]:
    #menghasilkan anak secara acak dengan menukar 2 elemen
    N = len(cube)
    i1, j1, k1 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    
    #untuk memastikan pertukarannya gasama
    while (i1, j1, k1) == (i2, j2, k2):
        i2, j2, k2 = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
    
    # Salin kubus untuk tetangga baru
    new_cube = [[[cube[i][j][k] for k in range(N)] for j in range(N)] for i in range(N)]
    
    # tukar elemen
    swap_elements(new_cube, (i1, j1, k1), (i2, j2, k2))
    
    return new_cube

def random_restart_algorithm(cube: List[List[List[int]]], max_restart: int = 10, max_iterations: int = 100) -> dict:
    """
    Melakukan algoritma random restart untuk meminimalkan cost kubus dengan mempertahankan variabel asli.
    Setiap restart memiliki batas maksimal iterasi, dan best_cube dibandingkan antar-restart.
    """
    N = len(cube)
    current_cube = utils.initialize_random_cube(N)
    current_cost = utils.objective_function(current_cube)
    cube = current_cube
    best_cost = current_cost
    restart = 0
    total_iteration = 0
    costs = []
    states = []
    iteration_restart = []
    
    start_time = time.time()

    while restart < max_restart:
        iteration = 0
        while iteration < max_iterations:
            # melakukan Generate random neighbor
            neighbor_cube = generate_random_neighbor(current_cube)
            neighbor_cost = utils.objective_function(neighbor_cube)
            
            if neighbor_cost >= current_cost:
                iteration += 1
                costs.append(current_cost)
                states.append(copy.deepcopy(current_cube))
                # Jika biaya tetangga lebih buruk atau sama, keluar dari pencarian
                break
            else:
                # Jika tetangga lebih baik, update current_cube
                current_cube = neighbor_cube
                current_cost = neighbor_cost
            iteration += 1
            costs.append(current_cost)
            states.append(copy.deepcopy(current_cube))

        # Bandingkan best_cube di setiap restart setelah restart pertama
        if restart == 0:
            cube = current_cube
            best_cost = current_cost
        else:
            # Jika solusi restart saat ini lebih baik, update best_cube
            if current_cost < best_cost:
                cube = current_cube
                best_cost = current_cost

        iteration_restart.append(iteration)
        restart += 1

        # Restart pencarian dengan solusi acak yang baru
        current_cube = utils.initialize_random_cube(N)
        current_cost = utils.objective_function(current_cube)

    duration = time.time() - start_time

    return {                                                   
        "final_cube": cube,
        "final_cost": best_cost,
        "average_cost": round(best_cost/109, 4),
        "duration": round(duration, 2),
        "iteration": len(costs),
        "iteration_restart": iteration_restart,
        "restart": restart,
        "costs": costs,
        "states": states
    }