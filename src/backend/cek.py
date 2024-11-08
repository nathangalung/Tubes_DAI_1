import matplotlib.pyplot as plt
import numpy as np

# Contoh data dummy untuk tujuan ilustrasi
iterations = np.arange(1, 101)  # Misal ada 100 iterasi
avg_fitness_over_time = np.random.normal(50, 5, len(iterations))  # Nilai rata-rata tiap iterasi
max_fitness_over_time = avg_fitness_over_time - np.random.uniform(0, 10, len(iterations))  # Nilai maksimum tiap iterasi

# Plot Objective Function Maksimum dan Rata-Rata
plt.figure(figsize=(10, 6))
plt.plot(iterations, max_fitness_over_time, label='Objective Function Maksimum', linestyle='-', linewidth=2)
plt.plot(iterations, avg_fitness_over_time, label='Objective Function Rata-Rata', linestyle='--', linewidth=2)

# Jika ingin menambahkan plot per individu pada populasi:
# Misalkan data per individu dalam array 2D `individual_fitness` (misal shape [num_individu, num_iterasi])
# Contoh data dummy
num_individu = 10
individual_fitness = [avg_fitness_over_time + np.random.normal(0, 2, len(iterations)) for _ in range(num_individu)]

# Plot garis untuk tiap individu dengan transparansi
for ind_fitness in individual_fitness:
    plt.plot(iterations, ind_fitness, color='grey', alpha=0.3, linewidth=1)

# Menambahkan detail pada plot
plt.title('Plot Objective Function terhadap Jumlah Iterasi')
plt.xlabel('Jumlah Iterasi')
plt.ylabel('Nilai Objective Function')
plt.legend()
plt.grid(True)

# Memberi anotasi jika ada plot per individu
plt.text(1, min(avg_fitness_over_time) - 5, 'Garis abu-abu menunjukkan nilai per individu dalam populasi', 
         fontsize=10, color='grey', alpha=0.6)

plt.show()