import numpy as np
import random

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

def partial_objective_function(cube, i1, j1, k1, i2, j2, k2, current_cost):
    """
    Calculates the new cost after swapping two elements in the cube.
    
    Args:
    - cube (numpy array): The cube configuration.
    - i1, j1, k1 (int): Coordinates of the first element to swap.
    - i2, j2, k2 (int): Coordinates of the second element to swap.
    - current_cost (int): The current objective function cost before the swap.
    
    Returns:
    - new_cost (int): The updated cost after the swap.
    """
    # Calculate the cost before the swap for the two elements
    old_cost_1 = calculate_element_cost(cube, i1, j1, k1)
    old_cost_2 = calculate_element_cost(cube, i2, j2, k2)

    # Perform the swap
    cube[i1][j1][k1], cube[i2][j2][k2] = cube[i2][j2][k2], cube[i1][j1][k1]

    # Calculate the cost after the swap
    new_cost_1 = calculate_element_cost(cube, i1, j1, k1)
    new_cost_2 = calculate_element_cost(cube, i2, j2, k2)

    # Update the current cost with the difference in old and new costs
    new_cost = current_cost + (new_cost_1 - old_cost_1) + (new_cost_2 - old_cost_2)

    return new_cost