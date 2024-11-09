from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from algorithm import (
    initialize_random_cube,
    objective_function,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm,
    stochastic_algorithm,
    save_json
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
class CubeInitResponse(BaseModel):
    cube: list
    objective_value: int

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

@app.get("/initialize_cube", response_model=CubeInitResponse)
async def initialize_cube():
    """
    Endpoint to initialize a random cube and return with objective value.
    """
    initial_cube = initialize_random_cube(N)
    objective_value = objective_function(initial_cube)
    return {
        "cube": initial_cube,
        "objective_value": objective_value
    }

@app.post("/run_algorithm_with_plot")
async def run_algorithm_with_plot(request: AlgorithmRequest):
    """
    Run the selected algorithm, save the cost data, and return a plot of the objective function.
    """
    algorithm_function = algorithm_map.get(request.algorithm)
    if not algorithm_function:
        raise HTTPException(status_code=404, detail="Algorithm not found")

    # Use cube data directly as list
    cube_data = request.cube

    try:
        modified_cube, best_cost = algorithm_function(cube_data)
    except ValueError as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Algorithm function did not return the expected output.")

    plot_filename = f"{request.algorithm}_objective_function_plot.png"
    return FileResponse(plot_filename, media_type="image/png")

@app.on_event("startup")
async def clear_algorithm_results():
    """
    Clear algorithm results on server startup.
    """
    pass