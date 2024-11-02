from deap import base, creator, tools, algorithms
import numpy as np
import random
import time
from numba import njit, prange
from . import utils
from concurrent.futures import ThreadPoolExecutor
# from .utils import plot_objective_function_progress
from copy import deepcopy

# Populasi dan iterasi dengan nilai yang lebih besar
POPULATION_OPTIONS = [100, 200, 300]  # Variasi ukuran populasi yang lebih besar untuk eksperimen yang maksimal
ITERATION_OPTIONS = [500, 1000, 1500]   # Variasi jumlah iterasi yang lebih besar untuk eksperimen yang maksimal
TOURNAMENT_SIZE = 10
INITIAL_ELITISM = 15
initial_mutation_rate = 0.05
mutation_rate = initial_mutation_rate
initial_crossover_rate = 0.9
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


def create_toolbox(cube, executor, population_size):
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


def adjust_mutation_and_crossover_rate(population, iteration_index, population_size):
    global mutation_rate, crossover_rate
    unique_fitness_values = len(set(ind.fitness.values[0] for ind in population if ind.fitness.valid))
    
    if unique_fitness_values < population_size / 4:
        mutation_rate = min(0.3, mutation_rate * 1.1)
        crossover_rate = max(0.7, crossover_rate * 0.95)
    else:
        mutation_rate = max(0.01, mutation_rate * 0.9)
        crossover_rate = min(0.95, crossover_rate * 1.05)


def restart_population(population, toolbox, population_size):
    restart_count = int(population_size * 0.3)
    new_individuals = [toolbox.individual() for _ in range(restart_count)]
    population[-restart_count:] = new_individuals


def dynamic_elitism(iteration_index, iteration_count):
    if iteration_index < iteration_count // 3:
        return INITIAL_ELITISM
    elif iteration_index < (2 * iteration_count) // 3:
        return int(INITIAL_ELITISM * 1.5)
    else:
        return int(INITIAL_ELITISM * 2)


def genetic_algorithm(cube):
    """
    Runs the genetic algorithm 9 times with different configurations of population sizes and iteration counts.
    
    Args:
    - cube: Initial state of the cube to solve.
    """
    pop_options = POPULATION_OPTIONS.copy()
    iter_options = ITERATION_OPTIONS.copy()
    
    experiments_completed = 0

    while experiments_completed < 9 and pop_options:
        # Prompt user to choose a population size
        print("\nJumlah Populasi tersedia:", pop_options)
        population_size = int(input("Pilih Jumlah Populasi: "))
        if population_size not in pop_options:
            print("Jumlah Populasi tidak  valid, silakan pilih Jumlah Populasi yang valid.")
            continue

        # Run 3 trials with different iteration counts for the chosen population size
        iter_trials = 0
        while iter_trials < 3 and iter_options:
            # Prompt user to choose an iteration count
            print("\nJumlah Iterasi tersedia:", iter_options)
            iteration_count = int(input("Pilih Jumlah Iterasi: "))
            if iteration_count not in iter_options:
                print("Jumlah Iterasi tidak  valid, silakan pilih Jumlah Iterasi yang valid.")
                continue
            
            # Use a copy of the initial cube state for each experiment
            initial_cube = deepcopy(cube)
            print(f"\nEksperimen dengan Jumlah Populasi = {population_size} dan Jumlah Iterasi = {iteration_count}")

            with ThreadPoolExecutor() as executor:
                toolbox = create_toolbox(initial_cube, executor, population_size)
                population = toolbox.population(n=population_size)
                hof = CustomHallOfFame(INITIAL_ELITISM)
                stats = tools.Statistics(lambda ind: ind.fitness.values)
                stats.register("avg", np.mean)
                stats.register("min", np.min)

                start_time = time.time()
                best_fitness, no_improvement_count = float('inf'), 0
                avg_fitness_over_time = []
                
                for iter_idx in range(iteration_count):
                    elitism_size = dynamic_elitism(iter_idx, iteration_count)
                    population = algorithms.varAnd(population, toolbox, cxpb=crossover_rate, mutpb=mutation_rate)

                    invalid_ind = [ind for ind in population if not ind.fitness.valid]
                    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                    for ind, fit in zip(invalid_ind, fitnesses):
                        ind.fitness.values = fit

                    offspring = toolbox.select(population + list(hof), k=population_size - elitism_size)
                    population[:] = offspring + list(hof)

                    adjust_mutation_and_crossover_rate(population, iter_idx, population_size)
                    avg_fitness = stats.compile(population)["avg"]

                    avg_fitness_over_time.append(avg_fitness)
                    current_best_fitness = min(ind.fitness.values[0] for ind in population)
                    
                    if current_best_fitness < best_fitness:
                        best_fitness = current_best_fitness
                        no_improvement_count = 0
                    else:
                        no_improvement_count += 1

                    if no_improvement_count > 50:
                        restart_population(population, toolbox, population_size)
                        no_improvement_count = 0

                    hof.update(population)

                    if hof[0].fitness.values[0] <= 1e-3:
                        break

                end_time = time.time()
                best_individual = hof[0]
                duration = end_time - start_time

                # # Plot the objective function over time for this experiment
                # plot_objective_function_progress(
                #     avg_fitness_over_time=avg_fitness_over_time,
                #     title=f'Genetic Algorithm (Pop Size={population_size}, Iterations={iteration_count})'
                # )

                # Print results for this experiment
                print("Initial Cube State:")
                utils.print_cube(initial_cube)  # Print the original initial state
                print("Final Cube State:")
                utils.print_cube(best_individual)
                print(f"Nilai Objective Function: {best_fitness}")
                print(f"Jumlah Populasi: {population_size}, Jumlah Iterasi: {iteration_count}")
                print(f"Durasi Eksperimen: {duration:.2f} detik\n")

            # Increment iteration trial counter and remove used iteration option
            iter_trials += 1
            iter_options.remove(iteration_count)
            experiments_completed += 1

        # Remove the population size option if all iteration trials are done or all iteration options are used
        if iter_trials == 3 or not iter_options:
            pop_options.remove(population_size)
            iter_options = ITERATION_OPTIONS.copy()  # Reset iteration options for the next population size
