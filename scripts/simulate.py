import argparse
import time

from moran.graph_utils import load_graph
from moran.simulation import simulation_from_mutants


def main():
    parser = argparse.ArgumentParser(
        description="Simulate the spread of a mutation in a graph (broadcast)."
    )
    parser.add_argument("-e", "--edges", default="examples/edges.in")
    parser.add_argument("-m", "--mutants", default="examples/mutants.in")
    parser.add_argument("-r", "--mutant_fitness", default=1, type=float)
    parser.add_argument("-s", "--simulations", default=1, type=int)
    parser.add_argument("--visualize", action="store_true")
    arguments = parser.parse_args()

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
