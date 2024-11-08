import numpy as np
import time
import matplotlib.pyplot as plt
from typing import Tuple
from . import utils

def swap_elements(cube: np.ndarray, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int], calculate_cost: bool = False) -> int:
    # Melakukan pertukaran elemen di posisi yang ditentukan
    i, j, k = pos1
    l, m, n = pos2
    cube[i, j, k], cube[l, m, n] = cube[l, m, n], cube[i, j, k]

    # Jika calculate_cost=True, hitung biaya dari konfigurasi baru
    if calculate_cost:
        cost = utils.objective_function(cube)
        # Kembalikan pertukaran ke keadaan semula
        cube[i, j, k], cube[l, m, n] = cube[l, m, n], cube[i, j, k]
        return cost  # Mengembalikan biaya

    # Jika calculate_cost=False, tidak ada biaya yang dihitung
    return None  # Bisa juga return 0 untuk kompatibilitas

def find_best_neighbor(cube: np.ndarray, best_cost: int, max_sideways: int, sideways_moves: int) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
    # Fungsi untuk mencari tetangga terbaik dengan biaya minimum
    N = cube.shape[0]
    best_neighbor_cost = best_cost
    best_swap = (-1, -1, -1, -1, -1, -1)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                # Hitung biaya saat ini untuk elemen di posisi (i, j, k)
                current_cost = utils.objective_function(cube)
                
                for l in range(i, N):  
                    for m in (range(j, N) if i == l else range(N)):
                        for n in (range(k, N) if i == l and j == m else range(N)):
                            if (i == l and j == m and k == n):
                                continue  # Lewati jika elemen yang sama
                            
                            # Lakukan pertukaran dan hitung biaya total
                            swap_elements(cube, (i, j, k), (l, m, n))
                            new_cost = utils.objective_function(cube) + utils.objective_function(cube)
                            total_cost = best_cost - current_cost + new_cost

                            # Tentukan apakah pertukaran ini memberikan biaya yang lebih baik
                            if total_cost < best_neighbor_cost or (
                                total_cost == best_neighbor_cost and sideways_moves < max_sideways
                            ):
                                best_neighbor_cost = total_cost
                                best_swap = (i, j, k, l, m, n)

                            # Kembalikan pertukaran ke keadaan asli
                            swap_elements(cube, (i, j, k), (l, m, n))

    return best_neighbor_cost, best_swap

def sideways_move_algorithm(cube: np.ndarray, max_sideways: int = 100, max_iterations: int = 1000) -> Tuple[int, float, int, list]:
    # Fungsi utama untuk melakukan hill climbing dengan sideways moves dan batas iterasi
    current_cost = utils.objective_function(cube)  # Hitung seluruh kubus
    best_cost = current_cost
    best_cube = cube.copy()  # Simpan keadaan kubus dengan biaya terbaik
    # best_cost = utils.objective_function(cube)
    moves, sideways_moves = 0, 0

    # Melacak nilai objective function pada setiap iterasi untuk plotting
    costs = []

    # print("Keadaan Awal Kubus:")
    # utils.print_cube(cube)

    start_time = time.time()

    while moves < max_iterations:  # Tambahkan kondisi batas iterasi
        # Panggil fungsi yang sudah dioptimalkan untuk mencari tetangga terbaik
        best_neighbor_cost, best_swap = find_best_neighbor(cube, best_cost, max_sideways, sideways_moves)

        # Berhenti jika tidak ada perbaikan dan jumlah langkah samping mencapai batas
        if best_neighbor_cost >= best_cost and sideways_moves >= max_sideways:
            break

        # Tambah langkah samping jika biaya tetap sama
        if best_neighbor_cost == best_cost:
            sideways_moves += 1
        else:
            sideways_moves = 0  # Atur ulang langkah samping jika ditemukan perbaikan

        # Terapkan pertukaran terbaik yang ditemukan
        if best_swap != (-1, -1, -1, -1, -1, -1):
            i, j, k, l, m, n = best_swap
            swap_elements(cube, (i, j, k), (l, m, n))
            best_cost = best_neighbor_cost

        moves += 1
        costs.append(current_cost)

    # Menghitung waktu yang dibutuhkan
    duration = time.time() - start_time

    # Cetak hasil akhir
    print("\nKeadaan Akhir Kubus:")
    utils.print_cube(best_cube)  # Menampilkan kubus dengan best_cost
    print(f"Nilai Akhir Objective Function: {best_cost}")
    print(f"Durasi Waktu: {duration:.2f} detik")
    print(f"Total Langkah: {moves}")

    # Save costs to JSON file
    utils.save_json(costs, "sideways_costs.json")

    # Plot the costs over iterations
    utils.plot_function("sideways_costs.json", "sideways_objective_function_plot.png", "Iteration",
                        "Objective Function Cost", "Objective Function Cost per Iteration")

    return moves, duration, best_cost

# def main():
#     # Tentukan ukuran kubus
#     N = 5  # Misalnya ukuran 3x3x3

#     # Inisialisasi kubus dengan angka unik menggunakan fungsi dari utils
#     cube = utils.initialize_random_cube(N)
    
#     # Jalankan algoritma simulated annealing
#     best_cost, moves, duration = sideways_move_algorithm(cube)

# # Panggil fungsi main untuk menjalankan driver
# if __name__ == "__main__":
#     main()