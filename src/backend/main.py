from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
import io
import json
from algorithm import (
    initialize_random_cube,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    stochastic_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm,
    plot_objective_function,
    save_costs
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
    Run the selected algorithm, save the cost data, and return a plot of the objective function.
    """
    # Get the algorithm function based on the requested algorithm name
    algorithm_function = algorithm_map.get(request.algorithm)
    if not algorithm_function:
        raise HTTPException(status_code=404, detail="Algorithm not found")

    # Convert cube data from list to numpy array
    cube_data = np.array(request.cube)

    # Run the algorithm and get the modified cube and cost data
    try:
        modified_cube, best_cost = algorithm_function(cube_data)
    except ValueError as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Algorithm function did not return the expected output.")

    # Tentukan nama file PNG yang dinamis berdasarkan nama algoritma
    plot_filename = f"{request.algorithm}_objective_function_plot.png"

    # Save the costs and plot them with a dynamic filename
    save_costs(best_cost, filename=f"{request.algorithm}_costs.json")
    plot_objective_function(filename=f"{request.algorithm}_costs.json", plot_filename=plot_filename)

    # Return the file as a FileResponse instead of StreamingResponse
    return FileResponse(plot_filename, media_type="image/png")

@app.on_event("startup")
async def clear_algorithm_results():
    """
    Clear algorithm results on server startup.
    """
    # Placeholder function; additional startup configurations can be added here if needed
    pass
