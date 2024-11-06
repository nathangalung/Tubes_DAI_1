import numpy as np
import random
import time
import matplotlib.pyplot as plt

# Ukuran kubus dan magic number
n = 5
magic_number = (n * (n**3 + 1)) // 2

# Inisialisasi kubus acak dengan angka dari 1 hingga 125
def generate_initial_cube(n):
    numbers = list(range(1, n**3 + 1))
    random.shuffle(numbers)
    return np.array(numbers).reshape((n, n, n))

# Hitung deviasi dari magic number untuk sebuah kubus
def calculate_deviation(cube):
    deviation = 0
    # Baris, kolom, tiang
    for i in range(n):
        for j in range(n):
            deviation += abs(sum(cube[i, j, :]) - magic_number) # Baris
            deviation += abs(sum(cube[i, :, j]) - magic_number) # Kolom
            deviation += abs(sum(cube[:, i, j]) - magic_number) # Tiang

    # Diagonal ruang
    diag_space_1 = sum(cube[i, i, i] for i in range(n))
    diag_space_2 = sum(cube[i, i, n-i-1] for i in range(n))
    diag_space_3 = sum(cube[i, n-i-1, i] for i in range(n))
    diag_space_4 = sum(cube[i, n-i-1, n-i-1] for i in range(n))
    deviation += abs(diag_space_1 - magic_number)
    deviation += abs(diag_space_2 - magic_number)
    deviation += abs(diag_space_3 - magic_number)
    deviation += abs(diag_space_4 - magic_number)

    # Diagonal pada potongan bidang
    for i in range(n):
        deviation += abs(sum(cube[i, j, j] for j in range(n)) - magic_number)
        deviation += abs(sum(cube[j, i, j] for j in range(n)) - magic_number)
        deviation += abs(sum(cube[j, j, i] for j in range(n)) - magic_number)
        deviation += abs(sum(cube[i, j, n-j-1] for j in range(n)) - magic_number)
        deviation += abs(sum(cube[j, i, n-j-1] for j in range(n)) - magic_number)
        deviation += abs(sum(cube[j, n-j-1, i] for j in range(n)) - magic_number)
    
    return deviation

# Fungsi pertukaran dua angka
def swap(cube, pos1, pos2):
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]

# Algoritma Steepest Ascent Hill Climbing dengan keluaran tambahan
def steepest_ascent_algorithm(cube, max_iterations=10000):
    start_time = time.time()
    current_deviation = calculate_deviation(cube)
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
            new_deviation = calculate_deviation(cube)
            
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
        
        # Berhenti jika solusi ditemukan
        if current_deviation == 0:
            end_time = time.time()
            print(f"Solution found in {iteration + 1} iterations!")
            print(f"Duration: {end_time - start_time:.4f} seconds")
            return cube, deviations, initial_cube, current_deviation, iteration + 1, end_time - start_time

    # Jika batas iterasi tercapai tanpa solusi optimal
    end_time = time.time()
    print("Reached maximum iterations without finding an optimal solution.")
    return cube, deviations, initial_cube, current_deviation, max_iterations, end_time - start_time

# Inisialisasi dan jalankan algoritma
cube = generate_initial_cube(n)
result_cube, deviations, initial_cube, final_deviation, total_iterations, duration = steepest_ascent_algorithm(cube)

# Menampilkan hasil
print("Initial Cube State:")
print(initial_cube)
print("\nFinal Cube State:")
print(result_cube)
print(f"\nFinal Objective Function Value: {final_deviation}")
print(f"Total Iterations: {total_iterations}")
print(f"Search Duration: {duration:.4f} seconds")

# Plotting nilai objective function terhadap banyak iterasi
plt.plot(deviations)
plt.xlabel("Iterations")
plt.ylabel("Objective Function Value (Deviation)")
plt.title("Objective Function Value vs Iterations")
plt.show()
