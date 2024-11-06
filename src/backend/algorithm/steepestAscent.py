import numpy as np
import random
import time
import matplotlib.pyplot as plt
from . import utils

# Fungsi pertukaran dua angka
def swap(cube, pos1, pos2):
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]

# Algoritma Steepest Ascent Hill Climbing dengan keluaran tambahan
def steepest_ascent_algorithm(cube, max_iterations=10000):
    n = cube.shape[0]
    start_time = time.time()
    current_deviation = utils.objective_function(cube)
    initial_cube = np.copy(cube)
    deviations = [current_deviation]
    
    for iteration in range(max_iterations):
        best_deviation = current_deviation
        best_swap = None
        
        # Cari pasangan pertukaran terbaik
        for _ in range(100):  # Coba 100 pasangan secara acak
            pos1 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
            pos2 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
            
            if pos1 == pos2:
                continue
            
            # Lakukan pertukaran sementara
            swap(cube, pos1, pos2)
            new_deviation = utils.objective_function(cube)
            
            # Jika perbaikan ditemukan
            if new_deviation < best_deviation:
                best_deviation = new_deviation
                best_swap = (pos1, pos2)
            
            # Kembalikan pertukaran sementara
            swap(cube, pos1, pos2)
        
        # Jika perbaikan ditemukan, lakukan pertukaran
        if best_swap:
            swap(cube, best_swap[0], best_swap[1])
            current_deviation = best_deviation
            deviations.append(current_deviation)

    # Jika batas iterasi tercapai tanpa solusi optimal
    end_time = time.time()
    print(f"\nFinal Objective Function Value: {current_deviation}")
    print(f"Total Iterations: {iteration+1}")
    print(f"Search Duration: {end_time - start_time:.4f} seconds")
    plt.plot(deviations)
    plt.xlabel("Iterations")
    plt.ylabel("Objective Function Value (Deviation)")
    plt.title("Objective Function Value vs Iterations")
    plt.show()
    
    return cube # deviations, initial_cube, current_deviation, max_iterations, end_time - start_time

# # Inisialisasi dan jalankan algoritma
# result_cube, deviations, initial_cube, final_deviation, total_iterations, duration = steepest_ascent_algorithm(cube)

# # Menampilkan hasil
# print("Initial Cube State:")
# print(initial_cube)
# print("\nFinal Cube State:")
# print(result_cube)
# print(f"\nFinal Objective Function Value: {final_deviation}")
# print(f"Total Iterations: {total_iterations}")
# print(f"Search Duration: {duration:.4f} seconds")

# # Plotting nilai objective function terhadap banyak iterasi
# plt.plot(deviations)
# plt.xlabel("Iterations")
# plt.ylabel("Objective Function Value (Deviation)")
# plt.title("Objective Function Value vs Iterations")
# plt.show()
