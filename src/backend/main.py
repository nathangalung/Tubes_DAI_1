from algorithm import (
    initialize_random_cube,
    print_cube, objective_function,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    stochastic_algorithm,
    genetic_algorithm
)
from copy import deepcopy

N = 5

def main():
    initial_state_cube = initialize_random_cube(5)
    final_state_cube = [deepcopy(initial_state_cube) for _ in range(6)]
    
    print(f"Cost={objective_function(initial_state_cube)}")
    print_cube(initial_state_cube)

    print("Eksperimen Steepest Ascent Hill Climbing")
    steepest_ascent_algorithm(final_state_cube[0])
    print_cube(final_state_cube[0])

    print("Eksperimen Hill Climbing with Sideways Move")
    sideways_move_algorithm(final_state_cube[1])
    print_cube(final_state_cube[1])

    # print("Eksperimen Random Restart Hill Climbing")
    # random_restart_hill_climbing(final_state_cube[2])
    # print_cube(final_state_cube[2])

    # print("Eksperimen Simulated Annealing Algorithm")
    # simulated_annealing(final_state_cube[3])
    # print_cube(final_state_cube[3])

    print("Eksperimen Stochastic Hill Climbing Algorithm")
    final_state_cube[4] = stochastic_algorithm(final_state_cube[4])
    print_cube(final_state_cube[4])

    print("Eksperimen Genetic Algorithm")
    final_state_cube[5] = genetic_algorithm(final_state_cube[5])
    print_cube(final_state_cube[5])
    
if __name__ == "__main__":
    main()