import random
import time
from . import utils

# Fungsi pertukaran dua angka
def swap(cube, pos1, pos2):
    # Unpack tuples into individual indices
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    # Perform swap with proper list indexing
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

# Algoritma Steepest Ascent Hill Climbing dengan keluaran tambahan
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
        
        # Cari pasangan pertukaran terbaik
        for _ in range(100):  # Coba 100 pasangan secara acak
            pos1 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
            pos2 = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
            
            if pos1 == pos2:
                continue
            
            # Lakukan pertukaran sementara
            swap(cube, pos1, pos2)
            new_cost = utils.objective_function(cube)
            
            # Jika perbaikan ditemukan
            if new_cost < best_cost:
                best_cost = new_cost
                best_swap = (pos1, pos2)
            
            # Kembalikan pertukaran sementara
            swap(cube, pos1, pos2)
        
        # Jika perbaikan ditemukan, lakukan pertukaran
        if best_swap:
            swap(cube, best_swap[0], best_swap[1])
            current_cost = best_cost
            costs.append(current_cost)
        else:
            break  # Jika tidak ada perbaikan, keluar dari loop

    # Jika batas iterasi tercapai tanpa solusi optimal
    
    duration = time.time() - start_time
    
    return {
        "final_cube": cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs) + 1,
        "costs": costs
    }
