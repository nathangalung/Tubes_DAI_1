import random
import time
from . import utils

def steepest_ascent_algorithm(cube):
    N = cube.shape[0]
    best_cost = utils.objective_function(cube)
    moves = 0
    no_improvement = 0  # Counter untuk iterasi tanpa perbaikan
    MAX_NO_IMPROVEMENT = 100  # Batas maksimal iterasi tanpa perbaikan
    MAX_SEARCH_SIZE = N * N * N // 2  # Jumlah swap yang diuji dalam satu iterasi
    start_time = time.time()

    # Loop utama, berhenti jika tidak ada perbaikan setelah beberapa iterasi
    while no_improvement < MAX_NO_IMPROVEMENT:
        best_neighbor_cost = best_cost
        swap_coords = None

        # Cari swap terbaik
        for _ in range(MAX_SEARCH_SIZE):
            # Pilih dua elemen acak untuk di-swap
            i, j, k = random.randint(0, N - 1), random.randint(0, N - 1), random.randint(0, N - 1)
            l, m, n = random.randint(0, N - 1), random.randint(0, N - 1), random.randint(0, N - 1)

            # Lakukan swap sementara
            cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]
            current_cost = utils.objective_function(cube)

            # Cek jika ada perbaikan
            if current_cost < best_neighbor_cost:
                best_neighbor_cost = current_cost
                swap_coords = (i, j, k, l, m, n)

            # Kembalikan swap
            cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

        # Jika tidak ada perbaikan, tambah penghitung
        if best_neighbor_cost >= best_cost:
            no_improvement += 1
        else:
            # Terapkan swap terbaik jika ada perbaikan
            if swap_coords:
                i, j, k, l, m, n = swap_coords
                cube[i][j][k], cube[l][m][n] = cube[l][m][n], cube[i][j][k]

            # Update best_cost dan reset counter no_improvement
            best_cost = best_neighbor_cost
            no_improvement = 0

        moves += 1

    end_time = time.time()
    print(f"Steepest Ascent Hill Climbing: Moves={moves}, Time={end_time - start_time:.2f} seconds, Best Cost={best_cost}")

    return cube
