from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from copy import deepcopy
from pydantic import BaseModel

# Import algorithm functions
from algorithm import (
    initialize_random_cube,
    steepest_ascent_algorithm,
    sideways_move_algorithm,
    simulated_annealing_algorithm,
    stochastic_algorithm,
    genetic_algorithm
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

N = 5  # Cube dimension

class CubeResponse(BaseModel):
    cube: list

# Endpoint to initialize the cube
@app.get("/initialize_cube", response_model=CubeResponse)
async def initialize_cube():
    initial_cube = initialize_random_cube(N)
    return {"cube": initial_cube.tolist()}

# Helper function to run an algorithm and return its result
def run_algorithm(algorithm, cube_data):
    modified_cube = deepcopy(cube_data)  # Deep copy to avoid modifying the original data
    algorithm(modified_cube)
    return modified_cube.tolist()

# Endpoint for each algorithm

@app.post("/steepest_ascent", response_model=CubeResponse)
async def steepest_ascent(cube: CubeResponse):
    cube_data = np.array(cube.cube)
    result = run_algorithm(steepest_ascent_algorithm, cube_data)
    return {"cube": result}

@app.post("/sideways_move", response_model=CubeResponse)
async def sideways_move(cube: CubeResponse):
    cube_data = np.array(cube.cube)
    result = run_algorithm(sideways_move_algorithm, cube_data)
    return {"cube": result}

@app.post("/stochastic", response_model=CubeResponse)
async def stochastic(cube: CubeResponse):
    cube_data = np.array(cube.cube)
    result = run_algorithm(stochastic_algorithm, cube_data)
    return {"cube": result}

@app.post("/simulated_annealing", response_model=CubeResponse)
async def simulated_annealing(cube: CubeResponse):
    cube_data = np.array(cube.cube)
    result = run_algorithm(simulated_annealing_algorithm, cube_data)
    return {"cube": result}

@app.post("/genetic", response_model=CubeResponse)
async def genetic(cube: CubeResponse):
    cube_data = np.array(cube.cube)
    result = run_algorithm(genetic_algorithm, cube_data)
    return {"cube": result}
