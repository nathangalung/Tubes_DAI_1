# Import utility functions
from .utils import (
    initialize_random_cube,
    print_cube,
    calculate_magic_number,
    objective_function
)

from .steepestAscent import steepest_ascent_algorithm

from .sidewaysMove import sideways_move_algorithm

# Import stochastic algorithm functions
from .stochastic import stochastic_algorithm

# Import genetic algorithm and necessary components
from .genetic import genetic_algorithm

# from .steepestAscent import SteepestAscent
# from .sidwaysMove import SidewaysMove
# from .randomRestart import RandomRestart
# from .stochastic import Stochastic
# from .simulatedAnnealing import SimulatedAnnealing
# from .genetic import Genetic