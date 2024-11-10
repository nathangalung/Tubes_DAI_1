import time
import random
from typing import List, Tuple, Dict
from copy import deepcopy
from . import utils

def crossover(parent1: List[List[List[int]]], parent2: List[List[List[int]]], N: int) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if random.random() < 0.5:
                    child1[i][j][k], child2[i][j][k] = child2[i][j][k], child1[i][j][k]
    
    return child1, child2

def mutate(cube: List[List[List[int]]], N: int, mutation_rate: float = 0.1) -> List[List[List[int]]]:
    mutated = deepcopy(cube)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if random.random() < mutation_rate:
                    mutated[i][j][k] = random.randint(1, N * N * N)
    return mutated

def select_parents(population: List[List[List[List[int]]]], costs: List[float], n: int) -> List[List[List[List[int]]]]:
    selected = []
    for _ in range(n):
        idx1, idx2 = random.sample(range(len(population)), 2)
        if costs[idx1] < costs[idx2]:
            selected.append(deepcopy(population[idx1]))
        else:
            selected.append(deepcopy(population[idx2]))
    return selected

def genetic_algorithm(
    cube: List[List[List[int]]], 
    population_size: int = 200, 
    max_iterations: int = 1500,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.1
) -> Dict:
    N = len(cube)
    population = [utils.initialize_random_cube(N) for _ in range(population_size)]
    costs = []  # Track all costs across iterations
    costs_population = {}  # Track costs per population
    current_population = 1
    best_cost = float('inf')
    best_cube = None
    
    start_time = time.time()
    
    costs_population[f"population_{current_population}"] = []
    
    for iteration in range(max_iterations):
        # Evaluate population
        population_costs = [utils.objective_function(ind) for ind in population]
        current_best = min(population_costs)
        current_best_idx = population_costs.index(current_best)
        
        # Track costs
        costs.append(current_best)
        costs_population[f"population_{current_population}"].append(current_best)
        
        # Update best solution
        if current_best < best_cost:
            best_cost = current_best
            best_cube = deepcopy(population[current_best_idx])
        
        # Selection
        parents = select_parents(population, population_costs, population_size)
        
        # Crossover
        new_population = []
        for i in range(0, population_size-1, 2):
            if random.random() < crossover_rate:
                child1, child2 = crossover(parents[i], parents[i+1], N)
                new_population.extend([child1, child2])
            else:
                new_population.extend([parents[i], parents[i+1]])
        
        # Mutation
        for i in range(len(new_population)):
            new_population[i] = mutate(new_population[i], N, mutation_rate)
        
        population = new_population
        
        # Check if we should start new population
        if iteration > 0 and iteration % (max_iterations // population_size) == 0:
            current_population += 1
            costs_population[f"population_{current_population}"] = []
        
        if best_cost <= 1e-3:
            break
    
    duration = time.time() - start_time
    print(f"Duration: {duration}")
    
    return {
        "final_cube": best_cube,
        "final_cost": best_cost,
        "duration": round(duration, 2),
        "iterations": len(costs),
        "population": population_size,
        "costs": costs
    }