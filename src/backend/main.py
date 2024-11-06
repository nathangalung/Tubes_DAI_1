from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from copy import deepcopy
from pydantic import BaseModel
from algorithm import (
    initialize_random_cube,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    # random_restart_algorithm,
    stochastic_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

N = 5  # Dimension of the cube
algorithm_results = {}  # Dictionary to store results for each algorithm

class CubeResponse(BaseModel):
    cube: list

# Dictionary to map algorithm names to functions
algorithm_map = {
    'steepest_ascent': steepest_ascent_algorithm,
    'sideways_move': sideways_move_algorithm,
    # 'random_restart': random_restart_algorithm,
    'stochastic': stochastic_algorithm,
    'simulated_annealing': simulated_annealing_algorithm,
    'genetic': genetic_algorithm
}

@app.get("/initialize_cube", response_model=CubeResponse)
async def initialize_cube():
    initial_cube = initialize_random_cube(N)
    return {"cube": initial_cube.tolist()}

def run_algorithm(algorithm, cube_data):
    modified_cube = deepcopy(cube_data)
    algorithm(modified_cube)
    return modified_cube.tolist()

# Run all algorithms in sequence
@app.post("/run_all_algorithms", response_model=dict)
async def run_all_algorithms(cube: CubeResponse, background_tasks: BackgroundTasks):
    for name, algorithm_function in algorithm_map.items():
        background_tasks.add_task(execute_algorithm, name, cube.cube)
    return {"status": "running all algorithms"}

def execute_algorithm(algorithm_name, cube_data):
    """
    Execute a specified algorithm, storing the result in algorithm_results.
    """
    algorithm_function = algorithm_map.get(algorithm_name)
    if algorithm_function:
        result_cube = run_algorithm(algorithm_function, np.array(cube_data))
        algorithm_results[algorithm_name] = result_cube  # Store the result

@app.get("/get_algorithm_result/{algorithm_name}", response_model=CubeResponse)
async def get_algorithm_result(algorithm_name: str):
    """
    Retrieve the result of a specified algorithm if available.
    """
    result = algorithm_results.get(algorithm_name, [])
    return {"cube": result}

@app.on_event("startup")
async def clear_algorithm_results():
    """
    Clear algorithm results on server startup.
    """
    global algorithm_results
    algorithm_results = {}
