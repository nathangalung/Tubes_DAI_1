import time
import math
import matplotlib.pyplot as plt
import numpy as np
from . import utils

def swap_elements(cube, pos1, pos2):
    i1, j1, k1 = pos1
    i2, j2, k2 = pos2
    cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]

def get_random_neighbor(N):
    pos1 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    pos2 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    while pos1 == pos2:
        pos2 = (np.random.randint(N), np.random.randint(N), np.random.randint(N))
    return pos1, pos2

def acceptance_function(delta_cost, temperature):
    if delta_cost < 0:
        return True
    else:
        r = np.random.rand()
        if r < math.exp(-delta_cost / temperature):
            return True
        else:
            return False

def simulated_annealing_algorithm(cube, T_max=100.0, T_min=0.1, E_threshold=0.01, cooling_rate=0.9993,
                                  max_no_improvement=1000, max_iterations=10000):
    current_cost = utils.objective_function(cube)  # Hitung seluruh kubus
    best_cost = current_cost
    best_cube = cube.copy()  # Simpan keadaan kubus dengan biaya terbaik
    temperature = T_max
    moves = 0
    no_improvement = 0
    local_optima_count = 0

    objective_history = []
    temperature_history = []

    print("Keadaan Awal Kubus:")
    utils.print_cube(cube)

    start_time = time.time()

    while temperature > T_min and current_cost > E_threshold and moves < max_iterations:
        pos1, pos2 = get_random_neighbor(cube.shape[0])
        swap_elements(cube, pos1, pos2)

        new_cost = utils.objective_function(cube)
        delta_cost = new_cost - current_cost

        if acceptance_function(delta_cost, temperature):
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                best_cube = cube.copy()
                no_improvement = 0  # Reset counter karena ada perbaikan
            else:
                no_improvement += 1
        else:
            swap_elements(cube, pos1, pos2)
            no_improvement += 1

        # Cek apakah sudah terlalu banyak iterasi tanpa perbaikan
        if no_improvement == max_no_improvement // 2:
            local_optima_count += 1  # Increment counter jika "stuck" di local optima

        if no_improvement >= max_no_improvement:
            break

        # Cool the temperature
        temperature *= cooling_rate

        # Store history for plotting
        objective_history.append(current_cost)
        temperature_history.append(temperature)

        moves += 1

    duration = time.time() - start_time

    print("\nKeadaan Akhir Kubus:")
    utils.print_cube(best_cube)  # Menampilkan kubus dengan best_cost
    print(f"\nNilai Akhir Objective Function: {best_cost}")
    print(f"Durasi Waktu: {duration:.2f} detik")
    print(f"Total Langkah: {moves}")
    print(f"Frekuensi 'Stuck' di Local Optima: {local_optima_count}")

    plt.figure(figsize=(10, 5))
    plt.plot(objective_history[:moves + 1])
    plt.xlabel("Iterasi")
    plt.ylabel("Nilai Objective Function")
    plt.title("Nilai Objective Function per Iterasi")
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(temperature_history[:moves + 1])
    plt.xlabel("Iterasi")
    plt.ylabel("E x T (Energi x Temperatur)")
    plt.title("Energi x Temperatur per Iterasi")
    plt.show()

    return best_cost, moves, duration