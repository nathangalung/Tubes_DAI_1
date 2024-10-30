# Import utility functions
from .utils import (
    initialize_random_cube,
    print_cube,
    calculate_magic_number,
    objective_function
)

# Import stochastic algorithm functions
from .stochastic import stochastic_hill_climbing

# Import genetic algorithm and necessary components
from .genetic import (
    genetic_algorithm  # Main function for running the genetic algorithm
)

# from .steepestAscent import SteepestAscent
# from .sidwaysMove import SidewaysMove
# from .randomRestart import RandomRestart
# from .stochastic import Stochastic
# from .simulatedAnnealing import SimulatedAnnealing
# from .genetic import Genetic    