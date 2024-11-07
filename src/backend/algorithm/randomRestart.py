import numpy as np
import random
import time
import matplotlib.pyplot as plt
from . import utils

# def random_initial_cube(n):
#     # Membuat array angka 1 hingga n^3 lalu mengacaknya untuk membuat kubus awal
#     numbers = list(range(1, n**3 + 1))
#     random.shuffle(numbers)
#     return np.array(numbers).reshape((n, n, n))

# def calculate_fitness(cube, magic_number):
#     # Menghitung fitness sebagai jumlah selisih antara jumlah tiap baris, kolom, tiang, dan diagonal dengan magic number
#     n = cube.shape[0]
#     fitness = 0
    
#     # Cek baris, kolom, dan tiang
#     for i in range(n):
#         for j in range(n):
#             fitness += abs(magic_number - np.sum(cube[i, j, :]))   # Baris
#             fitness += abs(magic_number - np.sum(cube[i, :, j]))   # Kolom
#             fitness += abs(magic_number - np.sum(cube[:, i, j]))   # Tiang

#     # Cek diagonal ruang
#     fitness += abs(magic_number - np.sum([cube[i, i, i] for i in range(n)]))
#     fitness += abs(magic_number - np.sum([cube[i, i, n-i-1] for i in range(n)]))
#     fitness += abs(magic_number - np.sum([cube[i, n-i-1, i] for i in range(n)]))
#     fitness += abs(magic_number - np.sum([cube[n-i-1, i, i] for i in range(n)]))
    
#     return fitness

def swap_two_random_positions(cube):
    # Mengacak dua posisi dalam kubus dan menukarnya
    n = cube.shape[0]
    pos1 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
    pos2 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    return cube

def random_restart_algorithm(n, max_restarts, max_iterations):
    start_time = time.time()
    
    best_cube = None
    best_score = float('inf')
    restart_counts = 0
    all_scores = []

    for restart in range(max_restarts):
        restart_counts += 1
        cube = utils.initialize_random_cube(n)
        initial_state = cube.copy()
        current_score = utils.objective_function(cube, utils.calculate_magic_number)
        scores_per_restart = [current_score]
        
        for iteration in range(max_iterations):
            new_cube = swap_two_random_positions(cube.copy())
            new_score = utils.objective_function(new_cube, utils.calculate_magic_number)
            
            if new_score < current_score:
                cube = new_cube
                current_score = new_score
            
            scores_per_restart.append(current_score)
            
            # Simpan solusi terbaik jika ditemukan
            if current_score < best_score:
                best_cube = cube.copy()
                best_score = current_score
            
            # Jika solusi sempurna (fitness score = 0) ditemukan
            if current_score == 0:
                break
        
        all_scores.extend(scores_per_restart)
        
        # Jika solusi ditemukan
        if current_score == 0:
            break

    end_time = time.time()
    duration = end_time - start_time
    
    # Plot objective function terhadap iterasi
    plt.plot(all_scores)
    plt.xlabel("Iterasi")
    plt.ylabel("Objective Function (Fitness Score)")
    plt.title("Objective Function terhadap Iterasi")
    plt.show()
    
    # Output hasil akhir
    print("State Awal Kubus:\n", initial_state)
    print("\nState Akhir Kubus:\n", best_cube)
    print("\nNilai Objective Function Akhir yang Dicapai:", best_score)
    print("\nDurasi Pencarian:", duration, "detik")
    print("\nBanyak Restart:", restart_counts)
    print("\nBanyak Iterasi per Restart:", max_iterations)

# Parameter untuk algoritma
n = 5                    # Ukuran sisi kubus
max_restarts = 10        # Maksimum jumlah restart
max_iterations = 1000    # Maksimum iterasi per restart

# Menjalankan algoritma
random_restart_algorithm(n, max_restarts, max_iterations)
