from deap import base, creator, tools, algorithms
import numpy as np
import random
import time
from numba import njit
from . import utils  # Pastikan utils memiliki initialize_random_cube dan objective_function

# Constants
POPULATION_SIZE = 300  # Ukuran populasi yang lebih besar
GENERATIONS = 1200     # Lebih banyak generasi
TOURNAMENT_SIZE = 10   # Ukuran turnamen yang lebih besar
ELITISM = 20           # Elitisme yang lebih besar
initial_mutation_rate = 0.05   # Mutation rate awal yang lebih besar
mutation_rate = initial_mutation_rate  # Gunakan nilai dinamis

# DEAP setup to create Individual class with a fitness attribute
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

class CustomHallOfFame(tools.HallOfFame):
    def update(self, population):
        for ind in population:
            is_similar = any(np.array_equal(ind, hofer) for hofer in self.items)
            if not is_similar:
                if len(self.items) < self.maxsize:
                    self.insert(ind)
                elif self.maxsize > 0 and ind.fitness > self.items[-1].fitness:
                    self.items.pop(-1)
                    self.insert(ind)

def create_toolbox(cube):
    N = cube.shape[0]
    toolbox = base.Toolbox()

    def initialize_individual():
        individual = np.asarray(utils.initialize_random_cube(N), dtype=np.int32)
        return creator.Individual(individual)

    toolbox.register("individual", initialize_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda individual: (utils.objective_function(np.array(individual)),))
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    toolbox.register("mate", lambda ind1, ind2: [creator.Individual(child) for child in multi_parent_crossover([ind1, ind2], N)])
    toolbox.register("mutate", lambda ind: (adaptive_gaussian_mutate(ind, N),))

    return toolbox

@njit
def multi_parent_crossover(parents, N):
    """Multi-parent crossover to improve diversity."""
    num_parents = len(parents)
    child1 = np.copy(parents[0])
    child2 = np.copy(parents[1])
    
    for i in range(N):
        for j in range(N):
            for k in range(N):
                chosen_parent = parents[np.random.randint(num_parents)]
                if np.random.rand() < 0.5:
                    child1[i, j, k] = chosen_parent[i, j, k]
                else:
                    child2[i, j, k] = chosen_parent[i, j, k]

    return child1, child2

@njit
def adaptive_gaussian_mutate(individual, N, scale=0.1):
    """Gaussian mutation to introduce small changes."""
    global mutation_rate
    num_mutations = max(1, int(N * N * N * mutation_rate))
    for _ in range(num_mutations):
        idx = (np.random.randint(0, N), np.random.randint(0, N), np.random.randint(0, N))
        individual[idx] += int(np.random.normal(0, scale * N))  # Gaussian perturbation

        # Manual clipping to ensure the value is within bounds
        if individual[idx] < 1:
            individual[idx] = 1
        elif individual[idx] > N * N * N:
            individual[idx] = N * N * N
    return individual

def adjust_mutation_rate(population):
    global mutation_rate
    unique_fitness_values = set(ind.fitness.values[0] for ind in population if ind.fitness.valid)
    unique_count = len(unique_fitness_values)

    if unique_count < POPULATION_SIZE / 3:  # More aggressive mutation if diversity is low
        mutation_rate = min(0.3, mutation_rate * 1.1)
    else:
        mutation_rate = max(0.01, mutation_rate * 0.9)

def restart_population(population, toolbox):
    """Randomly restart a fraction of the population to escape local optima."""
    restart_count = int(POPULATION_SIZE * 0.4)  # Restart 40% of the population
    new_individuals = [toolbox.individual() for _ in range(restart_count)]
    population[-restart_count:] = new_individuals

def genetic_algorithm(cube):
    N = cube.shape[0]
    toolbox = create_toolbox(cube)
    population = toolbox.population(n=POPULATION_SIZE)
    
    hof = CustomHallOfFame(ELITISM)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    start_time = time.time()
    no_improvement_count = 0
    best_fitness = float('inf')
    
    for generation in range(GENERATIONS):
        population = algorithms.varAnd(population, toolbox, cxpb=0.9, mutpb=mutation_rate)

        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        offspring = toolbox.select(population + list(hof), k=POPULATION_SIZE - ELITISM)
        population[:] = offspring + list(hof)

        adjust_mutation_rate(population)

        # Restart population if there's no improvement over several generations
        current_best_fitness = min([ind.fitness.values[0] for ind in population])
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count > 50:  # Restart after 50 generations without improvement
            restart_population(population, toolbox)
            print(f"Population restarted at generation {generation}")
            no_improvement_count = 0

        hof.update(population)

        if generation % 50 == 0 and len(hof) > 0:
            best_fitness = hof[0].fitness.values[0]
            print(f"Generation {generation}: Best Fitness = {best_fitness}")

        if len(hof) > 0 and hof[0].fitness.values[0] <= 1e-3:
            print("Optimal solution found.")
            break

    end_time = time.time()
    if len(hof) > 0:
        best_individual = hof[0]
        print(f"Genetic Algorithm Complete: Time={end_time - start_time:.2f} seconds, Best Fitness={best_individual.fitness.values[0]}")
        return best_individual  # Return best individual found
    else:
        print("No valid solution found.")
        return None
