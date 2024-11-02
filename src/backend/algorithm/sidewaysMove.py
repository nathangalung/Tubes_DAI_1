import numpy as np
import time
import matplotlib.pyplot as plt  # Untuk plotting
from typing import Tuple

# Import fungsi-fungsi dari utils
from utils import initialize_random_cube, print_cube, calculate_magic_number, objective_function, calculate_element_cost

def swap_elements(cube: np.ndarray, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> None:
    # Fungsi untuk menukar elemen antara dua posisi di kubus
    i, j, k = pos1
    l, m, n = pos2
    cube[i, j, k], cube[l, m, n] = cube[l, m, n], cube[i, j, k]

def swap_and_calculate_cost(cube: np.ndarray, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> int:
    # Fungsi untuk menukar elemen sementara, menghitung biaya, lalu mengembalikan ke posisi awal
    swap_elements(cube, pos1, pos2)  # Melakukan pertukaran elemen
    cost = objective_function(cube)  # Menghitung biaya berdasarkan konfigurasi setelah pertukaran
    swap_elements(cube, pos1, pos2)  # Mengembalikan ke konfigurasi awal
    return cost

def find_best_neighbor_optimized(cube: np.ndarray, best_cost: int, max_sideways: int, sideways_moves: int) -> Tuple[int, Tuple[int, int, int, int, int, int]]:
    # Fungsi untuk mencari tetangga terbaik dengan biaya minimum
    N = cube.shape[0]
    best_neighbor_cost = best_cost
    best_swap = (-1, -1, -1, -1, -1, -1)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                # Hitung biaya saat ini untuk elemen di posisi (i, j, k)
                current_cost = calculate_element_cost(cube, i, j, k)
                
                for l in range(i, N):  
                    for m in (range(j, N) if i == l else range(N)):
                        for n in (range(k, N) if i == l and j == m else range(N)):
                            if (i == l and j == m and k == n):
                                continue  # Lewati jika elemen yang sama
                            
                            # Lakukan pertukaran dan hitung biaya total
                            swap_elements(cube, (i, j, k), (l, m, n))
                            new_cost = calculate_element_cost(cube, i, j, k) + calculate_element_cost(cube, l, m, n)
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

def hill_climbing_with_sideways_move_optimized(cube: np.ndarray, max_sideways: int = 100, max_iterations: int = 1000) -> Tuple[int, float, int, list]:
    # Fungsi utama untuk melakukan hill climbing dengan sideways moves dan batas iterasi
    N = cube.shape[0]
    best_cost = objective_function(cube)
    moves, sideways_moves = 0, 0
    start_time = time.time()

    # Cetak keadaan awal kubus
    print("Keadaan Awal Kubus:")
    print_cube(cube)

    # Melacak nilai objective function pada setiap iterasi untuk plotting
    cost_history = [best_cost]

    while moves < max_iterations:  # Tambahkan kondisi batas iterasi
        # Panggil fungsi yang sudah dioptimalkan untuk mencari tetangga terbaik
        best_neighbor_cost, best_swap = find_best_neighbor_optimized(cube, best_cost, max_sideways, sideways_moves)

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
        cost_history.append(best_cost)  # Melacak biaya terbaik per iterasi

    # Menghitung waktu yang dibutuhkan
    time_elapsed = time.time() - start_time

    # Cetak hasil akhir
    print("Keadaan Akhir Kubus:")
    print_cube(cube)  # Cetak keadaan akhir kubus
    print(f"Nilai Akhir Objective Function: {best_cost}")
    print(f"Durasi Waktu: {time_elapsed:.2f} detik")
    print(f"Total Langkah: {moves}")

    # Plot nilai objective function terhadap iterasi
    plt.plot(cost_history)
    plt.xlabel("Iterasi")
    plt.ylabel("Nilai Objective Function")
    plt.title("Nilai Objective Function per Iterasi")
    plt.show()

    return moves, time_elapsed, best_cost, cost_history