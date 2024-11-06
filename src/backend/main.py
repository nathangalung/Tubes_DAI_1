from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import numpy as np
from algorithm import (
    initialize_random_cube,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    stochastic_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm
)
from utils import plot_objective_function  # Import fungsi plot dari utils.py

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Size of the cube (dimension)
N = 5  # Adjust as needed

# Model for request and response
class CubeResponse(BaseModel):
    cube: list  # List to represent the 3D cube array

class AlgorithmRequest(BaseModel):
    algorithm: str  # Name of the algorithm to run
    cube: list  # Cube data to process

# Dictionary to map algorithm names to their functions
algorithm_map = {
    'steepest_ascent': steepest_ascent_algorithm,
    'sideways_move': sideways_move_algorithm,
    'stochastic': stochastic_algorithm,
    'simulated_annealing': simulated_annealing_algorithm,
    'genetic': genetic_algorithm
}

@app.get("/initialize_cube", response_model=CubeResponse)
async def initialize_cube():
    """
    Endpoint to initialize a random cube of dimension N x N x N.
    """
    initial_cube = initialize_random_cube(N)
    return {"cube": initial_cube.tolist()}  # Convert numpy array to list for JSON serialization

@app.post("/run_algorithm_with_plot")
async def run_algorithm_with_plot(request: AlgorithmRequest):
    """
    Run the selected algorithm and return a plot of the objective function per iteration.
    """
    # Get the algorithm function based on the requested algorithm name
    algorithm_function = algorithm_map.get(request.algorithm)
    if not algorithm_function:
        raise HTTPException(status_code=404, detail="Algorithm not found")

    # Convert cube data from list to numpy array
    cube_data = np.array(request.cube)

    # Run the algorithm and get the modified cube and best cost over iterations
    modified_cube, best_cost = algorithm_function(cube_data)

    # Generate and return the plot based on best_cost data
    return plot_objective_function(best_cost)

@app.on_event("startup")
async def clear_algorithm_results():
    """
    Clear algorithm results on server startup.
    """
    # Placeholder function; additional startup configurations can be added here if needed
    pass