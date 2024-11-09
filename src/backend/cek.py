import random
from typing import List

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

cube = initialize_random_cube(5)
print(len(cube))