from algorithm import initialize_random_cube, print_cube, objective_function, stochastic_hill_climbing, genetic_algorithm
from copy import deepcopy

N = 5

def main():
    
    cube = initialize_random_cube(5)
    cube1, cube2, cube3, cube4, cube5, cube6, cube7 = deepcopy(cube), deepcopy(cube), deepcopy(cube), deepcopy(cube), deepcopy(cube), deepcopy(cube), deepcopy(cube)
    
    print(f"Cost={objective_function(cube)}")
    print_cube(cube)

    # print("Testing Steepest Ascent Hill Climbing")
    # steepest_ascent_hill_climbing(cube1)
    # print_cube(cube1)

    # print("Testing Hill Climbing with Sideways Move")
    # hill_climbing_with_sideways_move(cube2)
    # print_cube(cube2)

    # print("Testing Random Restart Hill Climbing")
    # random_restart_hill_climbing(cube3)
    # print_cube(cube3)

    # print("Testing Simulated Annealing")
    # simulated_annealing(cube4)
    # print_cube(cube4)

    print("Testing Stochastic Hill Climbing")
    cube5 = stochastic_hill_climbing(cube5)
    print_cube(cube5)

    print("Testing Genetic Algorithm")
    cube6 = genetic_algorithm(cube6)
    print_cube(cube6)
    
if __name__ == "__main__":
    main()