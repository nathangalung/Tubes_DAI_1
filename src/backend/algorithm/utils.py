import random
from typing import List, Set, Tuple

def initialize_random_cube(N: int) -> List[List[List[int]]]:
    """Initializes a 3D cube with unique random integers"""
    total_cells = N * N * N
    used: Set[int] = set()
    cube = [[[0 for _ in range(N)] for _ in range(N)] for _ in range(N)]
    
    for i, j, k in [(i,j,k) for i in range(N) for j in range(N) for k in range(N)]:
        while (num := random.randint(1, total_cells)) in used:
            continue
        cube[i][j][k] = num
        used.add(num)
    
    return cube

def calculate_magic_number(N: int) -> int:
    """Calculates magic number for cube of size N"""
    return (N * (N**3 + 1)) // 2

def line_sum(cube: List[List[List[int]]], indices: List[Tuple[int, int, int]]) -> int:
    """Calculates sum of values along given indices"""
    return sum(cube[i][j][k] for i, j, k in indices)

def diagonal_indices(N: int, plane: str, i: int = 0) -> List[Tuple[int, int, int]]:
    """Returns indices for different types of diagonals"""
    if plane == "main":
        diagonals = [
            [(j, j, i) for j in range(N)],  # Top face
            [(j, N-1-j, i) for j in range(N)]
        ]
    elif plane == "face":
        diagonals = [
            [(i, j, j) for j in range(N)],  # Front face
            [(i, j, N-1-j) for j in range(N)]
        ]
    elif plane == "side":
        diagonals = [
            [(j, i, j) for j in range(N)],  # Side face
            [(j, i, N-1-j) for j in range(N)]
        ]
    else:  # space
        diagonals = [
            [(i, i, i) for i in range(N)],  # Main diagonal
            [(i, i, N-1-i) for i in range(N)],  # Anti-diagonal
            [(i, N-1-i, i) for i in range(N)],
            [(N-1-i, i, i) for i in range(N)]
        ]
    return diagonals

def objective_function(cube: List[List[List[int]]]) -> int:
    """Calculates total cost based on deviation from magic number"""
    N = len(cube)
    magic_number = calculate_magic_number(N)
    cost = 0

    # Line sums (rows, columns, pillars)
    for i in range(N):
        for j in range(N):
            row_indices = [(i, j, k) for k in range(N)]
            col_indices = [(i, k, j) for k in range(N)]
            pillar_indices = [(k, i, j) for k in range(N)]
            
            cost += abs(magic_number - line_sum(cube, row_indices))
            cost += abs(magic_number - line_sum(cube, col_indices))
            cost += abs(magic_number - line_sum(cube, pillar_indices))

    # Main space diagonals
    for diagonal in diagonal_indices(N, "main"):
        cost += abs(magic_number - line_sum(cube, diagonal))

    # Plane diagonals
    for i in range(N):
        for plane in ["face", "side", "top"]:
            for diagonal in diagonal_indices(N, plane, i):
                cost += abs(magic_number - line_sum(cube, diagonal))

    return cost