import copy
import time
import random
from typing import List, Tuple, Dict
from copy import deepcopy
from . import utils
from multiprocessing import Pool

def crossover(parent1: List[List[List[int]]], parent2: List[List[List[int]]], N: int) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if random.random() < 0.5:
                    child1[i][j][k], child2[i][j][k] = child2[i][j][k], child1[i][j][k]
    
    return child1, child2

def mutate(cube: List[List[List[int]]], N: int, mutation_rate: float) -> List[List[List[int]]]:
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
        tournament = random.sample(list(zip(population, costs)), k=3)
        winner = min(tournament, key=lambda x: x[1])
        selected.append(deepcopy(winner[0]))
    return selected

def evaluate_population(population: List[List[List[int]]]) -> List[float]:
    with Pool() as pool:
        costs = pool.map(utils.objective_function, population)
    return costs

def genetic_algorithm(
    cube: List[List[List[int]]], 
    population_size: int = 200, 
    max_iteration: int = 1500,
    crossover_rate: float = 0.8,
    initial_mutation_rate: float = 0.1,
    elitism_count: int = 5
) -> Dict:
    N = len(cube)
    population = [utils.initialize_random_cube(N) for _ in range(population_size)]
    costs = []
    costs_population = {}
    states = []
    best_cost = float('inf')
    best_cube = None
    mutation_rate = initial_mutation_rate
    
    start_time = time.time()
    
    for iteration in range(max_iteration):
        # Evaluate population
        population_costs = evaluate_population(population)
        current_best_cost = min(population_costs)
        current_best_idx = population_costs.index(current_best_cost)
        
        # Track costs and states
        costs.append(current_best_cost)
        states.append(deepcopy(population[current_best_idx]))
        
        # Update best solution
        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_cube = deepcopy(population[current_best_idx])
        
        # Elitism: preserve top elitism_count individuals
        sorted_population = sorted(zip(population, population_costs), key=lambda x: x[1])
        elites = [deepcopy(ind) for ind, _ in sorted_population[:elitism_count]]
        
        # Selection
        parents = select_parents(population, population_costs, population_size - elitism_count)
        
        # Crossover and mutation
        new_population = []
        for i in range(0, len(parents) - 1, 2):
            if random.random() < crossover_rate:
                child1, child2 = crossover(parents[i], parents[i+1], N)
            else:
                child1, child2 = deepcopy(parents[i]), deepcopy(parents[i+1])
            new_population.extend([mutate(child1, N, mutation_rate), mutate(child2, N, mutation_rate)])
        
        # Add elites to the new population
        population = elites + new_population[:population_size - elitism_count]
        
        # Gradually decrease mutation rate as solution improves
        mutation_rate = max(initial_mutation_rate * (0.99 ** iteration), 0.01)
        
        # Early stopping if satisfactory solution found
        if best_cost <= 1e-3:
            break
    
    duration = time.time() - start_time
    
    return {
        "final_cube": best_cube,
        "final_cost": best_cost,
        "average_cost": round(sum(costs) / len(costs), 4),
        "duration": round(duration, 2),
        "iteration": len(costs),
        "population": population_size,
        "costs": costs,
        "states": states,
    }