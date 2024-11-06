import time
import math
import matplotlib.pyplot as plt
import numpy as np
import utils

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

    costs = []
    temperature_history = []
    exp_delta_E_T_history = []
    iteration_list = []

    print("Keadaan Awal Kubus:")
    utils.print_cube(cube)

    start_time = time.time()

    while temperature > T_min and current_cost > E_threshold and moves < max_iterations:
        pos1, pos2 = get_random_neighbor(cube.shape[0])
        swap_elements(cube, pos1, pos2)

        new_cost = utils.objective_function(cube)
        delta_cost = new_cost - current_cost

        if acceptance_function(delta_cost, temperature):
            if delta_cost > 0:
                local_optima_count += 1

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

        if no_improvement >= max_no_improvement:
            break

        # Cool the temperature
        temperature *= cooling_rate

        # Store history for plotting
        costs.append(current_cost)
        temperature_history.append(temperature)

        if moves % 200 == 0:
            exp_delta_E_T = math.exp(-delta_cost / temperature) if delta_cost > 0 else 1
            exp_delta_E_T_history.append(exp_delta_E_T)
            iteration_list.append(moves)

        moves += 1

    duration = time.time() - start_time

    print("\nKeadaan Akhir Kubus:")
    utils.print_cube(best_cube)  # Menampilkan kubus dengan best_cost
    print(f"\nNilai Akhir Objective Function: {best_cost}")
    print(f"Durasi Waktu: {duration:.2f} detik")
    print(f"Total Langkah: {moves}")
    print(f"Frekuensi 'Stuck' di Local Optima: {local_optima_count}")

    # Save costs to JSON file
    utils.save_json(costs, "annealing_costs.json")
    utils.save_json(exp_delta_E_T_history, "annealing_probability.json")

    # Plot the costs over iterations
    utils.plot_function("annealing_costs.json", "annealing_objective_function_plot.png", "Iteration",
                        "Objective Function Cost", "Objective Function Cost per Iteration")
    utils.plot_function("annealing_probability.json", "annealing_probability_plot.png", "Iteration",
                        "$e^{\Delta E / T}$", "Plot $e^{\Delta E / T}$ per 200 Iteration")

    return best_cost, moves, duration

def main():
    # Tentukan ukuran kubus
    N = 5  # Misalnya ukuran 3x3x3

    # Inisialisasi kubus dengan angka unik menggunakan fungsi dari utils
    cube = utils.initialize_random_cube(N)
    
    # Jalankan algoritma simulated annealing
    best_cost, moves, duration = simulated_annealing_algorithm(cube)
    
    # Tampilkan hasil akhir
    print("\nHasil Simulated Annealing:")
    print(f"Biaya Terbaik: {best_cost}")
    print(f"Total Langkah: {moves}")
    print(f"Durasi: {duration:.2f} detik")

# Panggil fungsi main untuk menjalankan driver
if __name__ == "__main__":
    main()