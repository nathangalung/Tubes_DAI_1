from deap import base, creator, tools, algorithms
import numpy as np
import random
import time
from numba import njit, prange
from . import utils
from concurrent.futures import ThreadPoolExecutor

# Constants
POPULATION_SIZE = 300
GENERATIONS = 1500  # Increased for better convergence
TOURNAMENT_SIZE = 10
INITIAL_ELITISM = 15  # Reduced initial elitism, will adjust dynamically
initial_mutation_rate = 0.05
mutation_rate = initial_mutation_rate
initial_crossover_rate = 0.9  # Initial crossover rate
crossover_rate = initial_crossover_rate

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

class CustomHallOfFame(tools.HallOfFame):
    def update(self, population):
        for ind in population:
            if not any(np.array_equal(ind, hofer) for hofer in self.items):
                if len(self.items) < self.maxsize:
                    self.insert(ind)
                elif self.maxsize > 0 and ind.fitness > self.items[-1].fitness:
                    self.items.pop(-1)
                    self.insert(ind)

def create_toolbox(cube, executor):
    N = cube.shape[0]
    toolbox = base.Toolbox()

    def initialize_individual():
        return creator.Individual(np.asarray(utils.initialize_random_cube(N), dtype=np.int32))

    toolbox.register("individual", initialize_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: (utils.objective_function(np.array(ind)),))
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    toolbox.register("mate", lambda ind1, ind2: [creator.Individual(child) for child in multi_parent_crossover([ind1, ind2], N)])
    toolbox.register("mutate", lambda ind: (adaptive_gaussian_mutate(ind, N),))

    toolbox.register("map", executor.map)

    return toolbox

@njit(parallel=True)
def multi_parent_crossover(parents, N):
    num_parents = len(parents)
    child1, child2 = np.copy(parents[0]), np.copy(parents[1])
    
    for i in prange(N):
        for j in range(N):
            for k in range(N):
                chosen_parent = parents[random.randint(0, num_parents - 1)]
                if random.random() < 0.5:
                    child1[i, j, k] = chosen_parent[i, j, k]
                else:
                    child2[i, j, k] = chosen_parent[i, j, k]

    return child1, child2

@njit
def adaptive_gaussian_mutate(individual, N, scale=0.1):
    global mutation_rate
    num_mutations = max(1, int(N * N * N * mutation_rate))
    for _ in range(num_mutations):
        idx = (random.randint(0, N - 1), random.randint(0, N - 1), random.randint(0, N - 1))
        individual[idx] += int(np.random.normal(0, scale * N))
        individual[idx] = max(1, min(individual[idx], N * N * N))
    return individual

def adjust_mutation_and_crossover_rate(population, generation):
    global mutation_rate, crossover_rate
    unique_fitness_values = len(set(ind.fitness.values[0] for ind in population if ind.fitness.valid))
    
    if unique_fitness_values < POPULATION_SIZE / 4:
        mutation_rate = min(0.3, mutation_rate * 1.1)
        crossover_rate = max(0.7, crossover_rate * 0.95)
    else:
        mutation_rate = max(0.01, mutation_rate * 0.9)
        crossover_rate = min(0.95, crossover_rate * 1.05)

def restart_population(population, toolbox):
    restart_count = int(POPULATION_SIZE * 0.3)  # Restarting 30% of the population
    new_individuals = [toolbox.individual() for _ in range(restart_count)]
    population[-restart_count:] = new_individuals

def dynamic_elitism(generation):
    if generation < GENERATIONS // 3:
        return INITIAL_ELITISM
    elif generation < (2 * GENERATIONS) // 3:
        return int(INITIAL_ELITISM * 1.5)
    else:
        return int(INITIAL_ELITISM * 2)

def genetic_algorithm(cube):
    N = cube.shape[0]
    with ThreadPoolExecutor() as executor:
        toolbox = create_toolbox(cube, executor)
        population = toolbox.population(n=POPULATION_SIZE)
        hof = CustomHallOfFame(INITIAL_ELITISM)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)

        start_time = time.time()
        best_fitness, no_improvement_count = float('inf'), 0
        
        for generation in range(GENERATIONS):
            elitism_size = dynamic_elitism(generation)
            population = algorithms.varAnd(population, toolbox, cxpb=crossover_rate, mutpb=mutation_rate)

            invalid_ind = [ind for ind in population if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            offspring = toolbox.select(population + list(hof), k=POPULATION_SIZE - elitism_size)
            population[:] = offspring + list(hof)

            adjust_mutation_and_crossover_rate(population, generation)
            current_best_fitness = min(ind.fitness.values[0] for ind in population)
            
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if no_improvement_count > 50:
                restart_population(population, toolbox)
                no_improvement_count = 0

            hof.update(population)

            if generation % 50 == 0:
                best_fitness = hof[0].fitness.values[0]

            if hof[0].fitness.values[0] <= 1e-3:
                break

        end_time = time.time()
        best_individual = hof[0]
        print(f"Genetic Algorithm Complete: Time={end_time - start_time:.2f} seconds, Best Fitness={best_individual.fitness.values[0]}")
        return best_individual
