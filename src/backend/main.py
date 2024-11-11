from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from algorithm.utils import (
    initialize_random_cube,
    objective_function
)
from algorithm import (
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
SAVE_DIR = "./cube"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

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
    restart: int | None = None
    iteration_restart: list | None = None
    local_optima: int | None = None
    population: int | None = None
    costs: list
    states: list
    exps: list | None = None

class CubeData(BaseModel):
    file_name: str
    cube: list

class CubeCostRequest(BaseModel):
    cube: list

class CubeCostResponse(BaseModel):
    cost: int

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
            "states": result.get("states"),
            "exps": result.get("exps", None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate_cost", response_model=CubeCostResponse)
async def calculate_cost(request: CubeCostRequest):
    try:
        cost = objective_function(request.cube)
        return {"cost": cost}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save_cube")
async def save_cube(cube_data: CubeData):
    file_path = os.path.join(SAVE_DIR, f"{cube_data.file_name}.json")
    with open(file_path, "w") as file:
        json.dump({"magic_cube": cube_data.cube}, file)
    return {"message": "Cube saved successfully"}

@app.post("/load_cube", response_model=CubeInitResponse)
async def load_cube(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = json.loads(content)
        magic_cube = data.get("magic_cube")
        if not magic_cube or not isinstance(magic_cube, list):
            raise HTTPException(status_code=400, detail="Invalid cube format")

        # Check if the loaded cube meets the magic cube objective
        cost = objective_function(magic_cube)
        return {
            "initial_cube": magic_cube,
            "initial_cost": cost
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load cube: {str(e)}")