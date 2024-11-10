from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from algorithm import (
    initialize_random_cube,
    objective_function,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    stochastic_algorithm,
    random_restart_algorithm,
    simulated_annealing_algorithm,
    genetic_algorithm,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

N = 5

class CubeInitResponse(BaseModel):
    initial_cube: list
    initial_cost: int

class AlgorithmRequest(BaseModel):
    algorithm: str
    cube: list

class AlgorithmResponse(BaseModel):
    final_cube: list
    final_cost: int
    average_cost: float
    duration: float
    iteration: int
    restart: int | None = None  # Keep other optionals
    iteration_restart: list | None = None
    local_optima: int | None = None  # Make optional
    population: int | None = None
    costs: list
    exps: list | None = None  # Make optional

algorithm_map = {
    'steepest': steepest_ascent_algorithm,
    'sideways': sideways_move_algorithm,
    'stochastic': stochastic_algorithm,
    'random': random_restart_algorithm,
    'simulated': simulated_annealing_algorithm,
    'genetic': genetic_algorithm
}

@app.get("/initialize_cube", response_model=CubeInitResponse)
async def initialize_cube():
    initial_cube = initialize_random_cube(N)
    initial_cost = objective_function(initial_cube)
    return {
        "initial_cube": initial_cube,
        "initial_cost": initial_cost
    }

@app.post("/run_algorithm", response_model=AlgorithmResponse)
async def run_algorithm(request: AlgorithmRequest):
    algorithm_function = algorithm_map.get(request.algorithm)
    if not algorithm_function:
        raise HTTPException(status_code=404, detail="Algorithm not found")

    try:
        result = algorithm_function(request.cube)
        
        # Print the entire result dictionary for debugging
        print("Algorithm running completed")

        # Return with default None for optional fields if they are missing
        return {
            "final_cube": result.get("final_cube"),
            "final_cost": result.get("final_cost"),
            "average_cost": result.get("average_cost"),
            "duration": result.get("duration"),
            "iteration": result.get("iteration"),
            "restart": result.get("restart", None),
            "iteration_restart": result.get("iteration_restart", None),
            "local_optima": result.get("local_optima", None),
            "population": result.get("population", None),
            "costs": result.get("costs"),
            "exps": result.get("exps", None)  # Default to None if 'exps' key is missing
        }
    except Exception as e:
        print(f"Error in algorithm execution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
