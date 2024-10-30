import numpy as np
import random
import time
from . import utils

# Constants
POPULATION_SIZE = 50  # Reduced population size
GENERATIONS = 500
TOURNAMENT_SIZE = 3
ELITISM = 2

mutation_rate = 0.05  # Initial mutation rate

# Initialize population with random cubes
def initialize_population(N):
    return [{'cube': utils.initialize_random_cube(N), 'fitness': utils.objective_function(utils.initialize_random_cube(N))} 
            for _ in range(POPULATION_SIZE)]

# Tournament selection with a smaller tournament size
def tournament_selection(population):
    return min(random.sample(population, TOURNAMENT_SIZE), key=lambda ind: ind['fitness'])

# Optimized crossover with numpy
def crossover(parent1, parent2, N):
    child = -np.ones_like(parent1['cube'])
    map_vals = np.zeros(N * N * N, dtype=bool)

    # Copy a cycle of values from parent1
    idx = (child == -1)
    child[idx] = parent1['cube'][idx]
    map_vals[child[idx] - 1] = True

    # Fill from parent2 without duplicates
    idx = (child == -1)
    for val in parent2['cube'][idx].flat:
        if not map_vals[val - 1]:
            map_vals[val - 1] = True
            child[idx.flat][idx.argmax()] = val

    return {'cube': child, 'fitness': utils.objective_function(child)}

# Optimized mutation with numpy
def mutate(individual, N):
    num_mutations = max(1, int(N * N * N * mutation_rate))
    for _ in range(num_mutations):
        idx1 = tuple(np.random.randint(0, N, 3))
        idx2 = tuple(np.random.randint(0, N, 3))
        individual['cube'][idx1], individual['cube'][idx2] = individual['cube'][idx2], individual['cube'][idx1]
    individual['fitness'] = utils.objective_function(individual['cube'])

# Dynamic mutation rate adjustment
def adjust_mutation_rate(population):
    global mutation_rate
    unique_count = len(set(ind['fitness'] for ind in population))
    mutation_rate = min(0.15, mutation_rate * 1.1) if unique_count < POPULATION_SIZE / 2 else max(0.01, mutation_rate * 0.9)

# Main Genetic Algorithm
def genetic_algorithm(cube):
    N = cube.shape[0]
    population = initialize_population(N)
    generation = 0
    start_time = time.time()

    while generation < GENERATIONS:
        # Sort population by fitness and carry over elite individuals
        population.sort(key=lambda ind: ind['fitness'])
        new_population = population[:ELITISM]

        # Generate new population with crossover and mutation
        children = [crossover(tournament_selection(population), tournament_selection(population), N)
                    for _ in range(POPULATION_SIZE - ELITISM)]
        for child in children:
            mutate(child, N)

        new_population.extend(children)
        population = new_population

        # Adjust mutation rate based on diversity
        adjust_mutation_rate(population)

        # Check for best individual
        best_individual = min(population, key=lambda ind: ind['fitness'])
        
        # if generation % 10 == 0:
        #     print(f"Generation: {generation}, Best Fitness: {best_individual['fitness']}")

        if best_individual['fitness'] == 0:  # Stop if an optimal solution is found
            break

        generation += 1

    end_time = time.time()
    print(f"Genetic Algorithm Complete: Generations={generation}, Time={end_time - start_time:.2f} seconds, Best Fitness={best_individual['fitness']}")
    
    return best_individual['cube']
