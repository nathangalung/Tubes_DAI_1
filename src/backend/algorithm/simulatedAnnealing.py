import time
import math
import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from . import utils

@njit
def swap_elements(cube, pos1, pos2):
    # Menukar dua elemen di dalam kubus pada posisi yang ditentukan
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]

@njit
def get_random_positions(N):
    # Menghasilkan dua posisi acak yang berbeda dalam kubus NxNxN
    pos1 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    pos2 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    while pos1 == pos2:
        pos2 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    return pos1, pos2

@njit
def acceptance_probability(delta_cost, temperature):
    # Menghitung probabilitas penerimaan untuk solusi yang lebih buruk
    return math.exp(-delta_cost / temperature)

def simulated_annealing_algorithm(cube, initial_temperature=100.0, cooling_rate=0.9995, min_temperature=0.1,
                                  max_no_improvement=500, reheating_factor=1.2, max_iterations=10000):
    # Menginisialisasi array Numpy untuk melacak riwayat dengan ukuran tetap
    objective_history = np.zeros(max_iterations)
    energy_temp_history = np.zeros(max_iterations)

    # Menghitung biaya awal fungsi objektif
    current_cost = utils.objective_function(cube)
    best_cost = current_cost
    temperature = initial_temperature
    moves = 0
    no_improvement = 0
    local_optima_count = 0

    print("Keadaan Awal Kubus:")
    utils.print_cube(cube)

    start_time = time.time()

    for iteration in range(max_iterations):
        if temperature <= min_temperature or no_improvement >= max_no_improvement:
            break

        # Memilih dua posisi acak untuk ditukar
        pos1, pos2 = get_random_positions(cube.shape[0])

        # Melakukan pertukaran
        swap_elements(cube, pos1, pos2)

        # Menghitung biaya baru setelah pertukaran
        new_cost = utils.calculate_element_cost(cube, pos1[0], pos1[1], pos1[2]) + utils.calculate_element_cost(cube, pos2[0], pos2[1], pos2[2])
        delta_cost = new_cost - current_cost

        # Menerima keadaan baru berdasarkan kriteria penerimaan
        if delta_cost < 0 or np.random.rand() < acceptance_probability(delta_cost, temperature):
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                no_improvement = 0  # Reset jika ditemukan perbaikan
        else:
            # Membatalkan pertukaran jika tidak diterima
            swap_elements(cube, pos1, pos2)
            no_improvement += 1

        # Menghitung frekuensi saat 'stuck' di local optima
        if no_improvement == max_no_improvement / 2:
            local_optima_count += 1

        # Melacak riwayat untuk plotting
        objective_history[iteration] = current_cost
        energy_temp_history[iteration] = delta_cost * temperature

        # Hentikan jika solusi optimal ditemukan
        if best_cost == 0:
            break

        # Terapkan reheating jika 'stuck'
        if no_improvement > max_no_improvement / 2:
            temperature *= reheating_factor
            no_improvement = 0
        else:
            temperature *= cooling_rate

        moves += 1

    duration = time.time() - start_time

    # Menampilkan keadaan akhir kubus dan hasil akhir
    print("\nKeadaan Akhir Kubus:")
    utils.print_cube(cube)
    print(f"\nNilai Akhir Objective Function: {best_cost}")
    print(f"Durasi Waktu: {duration:.2f} detik")
    print(f"Total Langkah: {moves}")
    print(f"Frekuensi 'Stuck' di Local Optima: {local_optima_count}")

    # Plotting nilai objective function terhadap iterasi (hanya hingga iteration)
    plt.figure(figsize=(10, 5))
    plt.plot(objective_history[:iteration + 1])
    plt.xlabel("Iterasi")
    plt.ylabel("Nilai Objective Function")
    plt.title("Nilai Objective Function per Iterasi")
    plt.show()

    # Plotting Energi x Temperatur terhadap iterasi (hanya hingga iteration)
    plt.figure(figsize=(10, 5))
    plt.plot(energy_temp_history[:iteration + 1])
    plt.xlabel("Iterasi")
    plt.ylabel("E x T (Energi x Temperatur)")
    plt.title("Energi x Temperatur per Iterasi")
    plt.show()

    return best_cost, moves, duration