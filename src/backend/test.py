from copy import deepcopy
from algorithm import (
    initialize_random_cube,
    print_cube,
    objective_function,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    random_restart_algorithm,
    stochastic_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm
)

N = 5

cube = initialize_random_cube(N)
cubes = [deepcopy(cube) for _ in range(6)]

print("Eksperimen Initialize Random Cube")
print(f"Cost = {objective_function(cube)}")
print("Initial State:")
print_cube(cube)

print("Eksperimen Steepest Ascent Algorithm")
steepest_ascent_algorithm(cubes[0])
print_cube(cubes[0])

print("Eksperimen Sideways Move Algorithm")
sideways_move_algorithm(cubes[1])
print_cube(cubes[1])

print("Eksperimen Random Restart Algorithm")
random_restart_algorithm(cubes[2])
print_cube(cubes[2])

print("Eksperimen Stochastic Algorithm")
stochastic_algorithm(cubes[3])
print_cube(cubes[3])

print("Eksperimen Simulated Annealing Algorithm")
simulated_annealing_algorithm(cubes[4])
print_cube(cubes[4])

print("Eksperimen Genetic Algorithm")
genetic_algorithm(cubes[5])
print_cube(cubes[5])