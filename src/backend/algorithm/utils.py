import numpy as np
import random
import json
import matplotlib.pyplot as plt
import io

def save_costs(costs, filename="costs.json"):
    """
    Saves a list of costs to a file in JSON format.

    Args:
    - costs (list of int): List of cost values.
    - filename (str): File to save costs to.
    """
    # Convert all numpy.int64 values to Python's native int
    costs = [int(cost) for cost in costs]

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(costs, f)
    print(f"Costs saved to {filename}")

def initialize_random_cube(N):
    """
    Initializes a 3D cube of size N x N x N with unique random integers.
    
    Args:
    - N (int): Size of the cube.
    
    Returns:
    - cube (numpy array): Initialized random cube.
    """
    cube = np.zeros((N, N, N), dtype=int)
    used = set()  # Track used numbers

    for i in range(N):
        for j in range(N):
            for k in range(N):
                num = random.randint(1, N * N * N)
                while num in used:
                    num = random.randint(1, N * N * N)
                cube[i][j][k] = num
                used.add(num)

    return cube

def print_cube(cube):
    """
    Prints the cube in a readable format.
    
    Args:
    - cube (numpy array): The cube to print.
    """
    N = cube.shape[0]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                print(cube[i][j][k], end=' ')
            print()
        print()
    

def calculate_magic_number(N):
    """
    Calculates the magic number for a cube of size N.
    
    Args:
    - N (int): Size of the cube.
    
    Returns:
    - magic_number (int): The magic number.
    """
    return (N * (N**3 + 1)) // 2

def objective_function(cube):
    """
    Calculates the objective function cost based on deviation from the magic number.
    
    Args:
    - cube (numpy array): 3D cube configuration.
    
    Returns:
    - cost (int): Total cost or deviation from the magic number.
    """
    N = cube.shape[0]
    magic_number = calculate_magic_number(N)
    cost = 0

    # Iterate over each plane in the cube to calculate row, column, and pillar sums
    for i in range(N):
        for j in range(N):
            row_sum = np.sum(cube[i, j, :])  # Row (xy-plane)
            col_sum = np.sum(cube[i, :, j])  # Column (xz-plane)
            pillar_sum = np.sum(cube[:, i, j])  # Pillar (yz-plane)
            
            cost += abs(magic_number - row_sum)
            cost += abs(magic_number - col_sum)
            cost += abs(magic_number - pillar_sum)

    # Main space diagonals
    diag1 = np.sum([cube[i, i, i] for i in range(N)])  # (0,0,0) to (N-1,N-1,N-1)
    diag2 = np.sum([cube[i, i, N-i-1] for i in range(N)])  # (0,0,N-1) to (N-1,N-1,0)
    diag3 = np.sum([cube[i, N-i-1, i] for i in range(N)])  # (0,N-1,0) to (N-1,0,N-1)
    diag4 = np.sum([cube[N-i-1, i, i] for i in range(N)])  # (N-1,0,0) to (0,N-1,N-1)

    cost += abs(magic_number - diag1)
    cost += abs(magic_number - diag2)
    cost += abs(magic_number - diag3)
    cost += abs(magic_number - diag4)

    # Plane diagonals for each face
    # Front face (fixed x)
    for i in range(N):
        diag_front1 = np.sum([cube[i, j, j] for j in range(N)])  # Diagonal front face
        diag_front2 = np.sum([cube[i, j, N-1-j] for j in range(N)])  # Anti-diagonal front face
        cost += abs(magic_number - diag_front1)
        cost += abs(magic_number - diag_front2)

    # Side face (fixed y)
    for j in range(N):
        diag_side1 = np.sum([cube[i, j, i] for i in range(N)])  # Diagonal side face
        diag_side2 = np.sum([cube[i, j, N-1-i] for i in range(N)])  # Anti-diagonal side face
        cost += abs(magic_number - diag_side1)
        cost += abs(magic_number - diag_side2)

    # Top face (fixed z)
    for k in range(N):
        diag_top1 = np.sum([cube[i, i, k] for i in range(N)])  # Diagonal top face
        diag_top2 = np.sum([cube[i, N-1-i, k] for i in range(N)])  # Anti-diagonal top face
        cost += abs(magic_number - diag_top1)
        cost += abs(magic_number - diag_top2)

    return cost

def calculate_element_cost(cube, i, j, k):
    """
    Calculates the cost associated with a specific element in the cube.
    
    Args:
    - cube (numpy array): 3D cube configuration.
    - i, j, k (int): Coordinates of the element in the cube.
    
    Returns:
    - element_cost (int): The cost for that element's row, column, and diagonals.
    """
    N = cube.shape[0]
    magic_number = calculate_magic_number(N)
    element_cost = 0

    # Row (across x-axis)
    row_sum = np.sum(cube[:, j, k])
    element_cost += abs(magic_number - row_sum)

    # Column (across y-axis)
    col_sum = np.sum(cube[i, :, k])
    element_cost += abs(magic_number - col_sum)

    # Depth (across z-axis)
    depth_sum = np.sum(cube[i, j, :])
    element_cost += abs(magic_number - depth_sum)

    # Main diagonal (if applicable)
    if i == j == k:
        diag_sum = np.sum([cube[d, d, d] for d in range(N)])
        element_cost += abs(magic_number - diag_sum)

    # Anti-diagonal (if applicable)
    if i == j and k == N - 1 - i:
        anti_diag_sum = np.sum([cube[d, d, N-d-1] for d in range(N)])
        element_cost += abs(magic_number - anti_diag_sum)

    return element_cost

def plot_objective_function(filename="costs.json", plot_filename="objective_function_plot.png"):
    """
    Loads the cost values from a JSON file and plots the objective function values 
    per iteration, saving the plot as a PNG file.
    
    Args:
    - filename (str): Name of the JSON file containing the costs.
    - plot_filename (str): Name of the file to save the plot.
    """
    # Load costs from JSON file
    with open(filename, "r") as f:
        costs = json.load(f)
    
    # Plot iterations vs cost
    iterations = list(range(1, len(costs) + 1))  # Iterations are index+1
    
    plt.figure(figsize=(6, 4))
    plt.plot(iterations, costs, label="Objective Function")
    plt.xlabel("Iteration")
    plt.ylabel("Objective Function Cost")
    plt.title("Objective Function Cost per Iteration")
    plt.legend()
    
    # Save the plot as a PNG file
    plt.savefig(plot_filename, format='png')
    plt.close()
    print(f"Plot saved as {plot_filename}")

def run_algorithm(N, iterations):
    """
    Runs the cube initialization and objective function calculation over multiple iterations.
    
    Args:
    - N (int): Size of the cube.
    - iterations (int): Number of iterations to run.
    
    Returns:
    - None
    """
    cube = initialize_random_cube(N)
    costs = []

    for it in range(iterations):
        cost = objective_function(cube)
        costs.append(cost)
        print(f"Iteration {it + 1}, Cost = {cost}")

        # Update the cube with a new random configuration for next iteration
        cube = initialize_random_cube(N)

    # Save costs to file
    save_costs(costs)

# if __name__ == "__main__":
#     N = 5  # Ukuran cube
#     iterations = 10  # Jumlah iterasi

#     run_algorithm(N, iterations)

#     plot_objective_function("costs.json", "objective_function_plot.png")
