import argparse
import math
import time

from moran.graph_utils import load_graph
from moran.simulation import simulation_from_mutants


def main():
    parser = argparse.ArgumentParser(
        description="Simulate the spread of a mutation in a graph (broadcast)."
    )
    parser.add_argument("-e", "--edges", required=True)
    parser.add_argument("-m", "--mutants", required=True)
    parser.add_argument("-r", "--mutant_fitness", default=1, type=float)
    parser.add_argument("-s", "--simulations", default=1, type=int)
    parser.add_argument("--visualize", action="store_true")
    arguments = parser.parse_args()
    if arguments.simulations < 1:
        parser.error("Number of simulations must be at least 1.")
    if not math.isfinite(arguments.mutant_fitness) or arguments.mutant_fitness <= 0:
        parser.error("Mutant fitness must be a positive finite number.")

    start_time = time.perf_counter()
    graph = load_graph(arguments.edges, arguments.mutants)
    result = simulation_from_mutants(
        graph,
        mutant_fitness=arguments.mutant_fitness,
        num_simulations=arguments.simulations,
        visualize=arguments.visualize,
    )

    print(f"Fixation probability: {result.fixation_probability}")
    print(f"Absorption time: {result.absorption_time}")
    print(f"Conditional fixation time: {result.fixation_time}")
    print(f"Execution time: {time.perf_counter() - start_time} seconds")


if __name__ == "__main__":
    main()
