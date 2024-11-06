import numpy as np
import time
import random
from . import utils

def select_random_position(N):
    """Selects a random position in the cube."""
    return random.randint(0, N - 1)

def calculate_cost_change(cube, pos1, pos2):
    """
    Calculates the change in cost for a single swap between two positions.
    """
    original_cost = utils.objective_function(cube)
    # Perform the swap
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    # Calculate the new cost after the swap
    new_cost = utils.objective_function(cube)
    # Undo the swap to keep the cube unchanged
    cube[pos1], cube[pos2] = cube[pos2], cube[pos1]
    # Calculate the change in cost
    return new_cost - original_cost

def stochastic_algorithm(cube, max_moves=1000):
    """
    Performs stochastic hill climbing with a fixed number of iterations.
    """
    N = cube.shape[0]
    current_cube = cube
    current_cost = utils.objective_function(current_cube)
    moves = 0
    costs = []  # List to store the cost at each move for plotting

    start_time = time.time()

    while moves < max_moves:
        # Generate two random positions to swap
        pos1 = (select_random_position(N), select_random_position(N), select_random_position(N))
        pos2 = (select_random_position(N), select_random_position(N), select_random_position(N))
        
        # Ensure they are different positions
        while pos1 == pos2:
            pos2 = (select_random_position(N), select_random_position(N), select_random_position(N))

        # Calculate cost change
        cost_change = calculate_cost_change(current_cube, pos1, pos2)

        # Move to neighbor if it is better
        if cost_change < 0:
            # Perform the swap
            current_cube[pos1], current_cube[pos2] = current_cube[pos2], current_cube[pos1]
            current_cost += cost_change

        # Store current cost in the list for tracking
        costs.append(current_cost)
        moves += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Stochastic Hill Climbing: Moves={moves}, Time={elapsed_time:.2f} seconds, Final Cost={current_cost}")

    # # Save costs to JSON file
    # utils.save_costs(costs, "stochastic_costs.json")

    # # Plot the costs over iterations
    # utils.plot_objective_function("stochastic_costs.json", "stochastic_objective_function_plot.png")
    
    return current_cube, costs  # Return current_cube and costs list for frontend use