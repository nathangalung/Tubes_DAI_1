import numpy as np
import random
import json
import matplotlib.pyplot as plt
import io

def save_json(X, filename):
    """
    Saves a list of costs to a file in JSON format.

    Args:
    - costs (list of int): List of cost values.
    - filename (str): File to save costs to.
    """
    # Convert all numpy.int64 values to Python's native int
    X = [int(x) for x in X]

    # Save to JSON file
    with open(filename, "w") as f:
        json.dump(X, f)
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

def plot_function(filename, plot_filename, x_label, y_label, title):
    """
    Loads the cost values from a JSON file and plots the objective function values 
    per iteration, saving the plot as a PNG file.
    
    Args:
    - filename (str): Name of the JSON file containing the costs.
    - plot_filename (str): Name of the file to save the plot.
    """
    # Load costs from JSON file
    with open(filename, "r") as f:
        data = json.load(f)
    
# Determine the x-axis values (iterations)
    if filename == "annealing_probability.json":
        # If the filename indicates probability data, assume data points were taken every 200 iterations
        iterations = [i * 200 for i in range(1, len(data) + 1)]
    else:
        # For other files, plot per iteration
        iterations = list(range(1, len(data) + 1))
    
    plt.figure(figsize=(6, 4))
    plt.plot(iterations, data, label="Objective Function", color='blue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
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
    save_json(costs)

# if __name__ == "__main__":
#     N = 5  # Ukuran cube
#     iterations = 10  # Jumlah iterasi

#     run_algorithm(N, iterations)

#     plot_objective_function("costs.json", "objective_function_plot.png")
