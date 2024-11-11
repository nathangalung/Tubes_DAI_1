import copy
import random
from typing import List, Tuple, Dict
from copy import deepcopy
from algorithm import utils
import random
import time
from algorithm.utils import initialize_random_cube
from algorithm.genetic import genetic_algorithm

def crossover(parent1: List[List[List[int]]], parent2: List[List[List[int]]], N: int) -> List[List[List[int]]]:
    child = deepcopy(parent1)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if random.random() < 0.5:
                    child[i][j][k] = parent2[i][j][k]
    return child

def mutate(cube: List[List[List[int]]], N: int, mutation_rate: float) -> List[List[List[int]]]:
    mutated = deepcopy(cube)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if random.random() < mutation_rate:
                    mutated[i][j][k] = random.randint(1, N * N * N)
    return mutated

def evaluate_population(population: List[List[List[int]]]) -> List[float]:
    return [utils.objective_function(individual) for individual in population]

def tournament_selection(population: List[List[List[int]]], costs: List[float], tournament_size: int) -> List[List[List[int]]]:
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, costs)), k=tournament_size)
        winner = min(tournament, key=lambda x: x[1])
        selected.append(deepcopy(winner[0]))
    return selected

def genetic_algorithm(
    cube: List[List[List[int]]], 
    population_size: int = 300, 
    max_iteration: int = 1500,
    crossover_rate: float = 0.8,
    initial_mutation_rate: float = 0.05,
    elitism_count: int = 5,
    tournament_size: int = 5  # Increased tournament size for higher selection pressure
) -> Dict:
    N = len(cube)
    population = [utils.initialize_random_cube(N) for _ in range(population_size)]
    costs = []
    states = []
    best_cost = float('inf')
    best_cube = None
    
    initial_state = deepcopy(population[0])
    initial_fitness = utils.objective_function(initial_state)
    
    start_time = time.time()
    
    for iteration in range(max_iteration):
        # Evaluate population
        population_costs = evaluate_population(population)
        fitness_scores = list(zip(population_costs, population))
        fitness_scores.sort(key=lambda x: x[0])
        
        current_fitness_values = [score[0] for score in fitness_scores]
        avg_fitness = sum(current_fitness_values) / len(current_fitness_values)
        
        costs.append(avg_fitness)
        states.append(deepcopy(fitness_scores[0][1]))
        
        if fitness_scores[0][0] < best_cost:
            best_cost = fitness_scores[0][0]
            best_cube = deepcopy(fitness_scores[0][1])
        
        # Elitism: preserve top elitism_count individuals
        elites = [deepcopy(ind) for _, ind in fitness_scores[:elitism_count]]
        
        # Tournament selection
        selected_population = tournament_selection(population, population_costs, tournament_size)
        
        # Crossover and mutation
        next_population = []
        mutation_rate = initial_mutation_rate * (1 - iteration / max_iteration)  # Adaptive mutation rate
        while len(next_population) < population_size - elitism_count:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2, N)
            else:
                child = deepcopy(parent1)
            child = mutate(child, N, mutation_rate)
            next_population.append(child)
        
        # Add elites to the new population
        population = elites + next_population
        
        if best_cost <= 1e-3:
            break
        
        if iteration % 50 == 0:
            print(f"Iteration {iteration}: Best cost = {best_cost}")
    
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
    
N = 5
cube = initialize_random_cube(N)

# Run the genetic algorithm
result = genetic_algorithm(cube)

# Print the results
print("Best cost:", result["final_cost"])
print("Duration:", result["duration"])
print("Iterations:", result["iteration"])