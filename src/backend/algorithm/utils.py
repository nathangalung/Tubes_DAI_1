import random
import json
from typing import List

def save_json(X: List[int], filename: str) -> None:
    """
    Saves a list of costs to a file in JSON format.
    """
    with open(filename, "w") as f:
        json.dump(X, f)
    print(f"Costs saved to {filename}")

def initialize_random_cube(N: int) -> List[List[List[int]]]:
    """
    Initializes a 3D cube of size N x N x N with unique random integers.
    """
    cube = [[[0 for _ in range(N)] for _ in range(N)] for _ in range(N)]
    used = set()

    for i in range(N):
        for j in range(N):
            for k in range(N):
                num = random.randint(1, N * N * N)
                while num in used:
                    num = random.randint(1, N * N * N)
                cube[i][j][k] = num
                used.add(num)

    return cube

def print_cube(cube: List[List[List[int]]]) -> None:
    """
    Prints the cube in a readable format.
    """
    N = len(cube)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                print(cube[i][j][k], end=' ')
            print()
        print()

def calculate_magic_number(N: int) -> int:
    """
    Calculates the magic number for a cube of size N.
    """
    return (N * (N**3 + 1)) // 2

def sum_list(lst: List[int]) -> int:
    """Helper function to sum a list of numbers"""
    return sum(lst)

def objective_function(cube: List[List[List[int]]]) -> int:
    """
    Calculates the objective function cost based on deviation from the magic number.
    """
    N = len(cube)
    magic_number = calculate_magic_number(N)
    cost = 0

    # Row, column, and pillar sums
    for i in range(N):
        for j in range(N):
            row_sum = sum([cube[i][j][k] for k in range(N)])  # Row
            col_sum = sum([cube[i][k][j] for k in range(N)])  # Column
            pillar_sum = sum([cube[k][i][j] for k in range(N)])  # Pillar
            
            cost += abs(magic_number - row_sum)
            cost += abs(magic_number - col_sum)
            cost += abs(magic_number - pillar_sum)

    # Main space diagonals
    diag1 = sum([cube[i][i][i] for i in range(N)])
    diag2 = sum([cube[i][i][N-i-1] for i in range(N)])
    diag3 = sum([cube[i][N-i-1][i] for i in range(N)])
    diag4 = sum([cube[N-i-1][i][i] for i in range(N)])

    cost += abs(magic_number - diag1)
    cost += abs(magic_number - diag2)
    cost += abs(magic_number - diag3)
    cost += abs(magic_number - diag4)

    # Plane diagonals
    for i in range(N):
        # Front face
        diag_front1 = sum([cube[i][j][j] for j in range(N)])
        diag_front2 = sum([cube[i][j][N-1-j] for j in range(N)])
        cost += abs(magic_number - diag_front1)
        cost += abs(magic_number - diag_front2)

        # Side face
        diag_side1 = sum([cube[j][i][j] for j in range(N)])
        diag_side2 = sum([cube[j][i][N-1-j] for j in range(N)])
        cost += abs(magic_number - diag_side1)
        cost += abs(magic_number - diag_side2)

        # Top face
        diag_top1 = sum([cube[j][j][i] for j in range(N)])
        diag_top2 = sum([cube[j][N-1-j][i] for j in range(N)])
        cost += abs(magic_number - diag_top1)
        cost += abs(magic_number - diag_top2)

    return cost

# def plot_function(filename, plot_filename, x_label, y_label, title):
#     """
#     Loads the cost values from a JSON file and plots the objective function values 
#     per iteration, saving the plot as a PNG file.
    
#     Args:
#     - filename (str): Name of the JSON file containing the costs.
#     - plot_filename (str): Name of the file to save the plot.
#     """
#     # Load costs from JSON file
#     with open(filename, "r") as f:
#         data = json.load(f)
    
# # Determine the x-axis values (iterations)
#     if filename == "annealing_probability.json":
#         # If the filename indicates probability data, assume data points were taken every 200 iterations
#         iterations = [i * 200 for i in range(1, len(data) + 1)]
#     else:
#         # For other files, plot per iteration
#         iterations = list(range(1, len(data) + 1))
    
#     plt.figure(figsize=(6, 4))
#     plt.plot(iterations, data, label="Objective Function", color='blue')
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.title(title)
#     plt.legend()
    
#     # Save the plot as a PNG file
#     plt.savefig(plot_filename, format='png')
#     plt.close()
#     print(f"Plot saved as {plot_filename}")
