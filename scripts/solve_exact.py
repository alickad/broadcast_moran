import argparse
import math
import time

from moran.graph_utils import load_graph
from moran.exact_solver import main as solve

"""
This script solves the broadcast Moran process exactly for a given graph and initial mutants.
It reads the graph from an edge list file and the initial mutants from a separate file.
Usage:
    python solve_exact.py -e <edge_file> -m <mutant_file> -r <mutant_fitness>
Arguments:
    -e, --edges: The edge list file representing the graph.
    -m, --mutants: The file containing the initial mutants.
    -r, --mutant_fitness: The fitness of the mutants (default: 1.0).
"""
def main():
    parser = argparse.ArgumentParser(
        description="Solve the broadcast Moran process exactly."
    )
    parser.add_argument("-e", "--edges", required=True)
    parser.add_argument("-m", "--mutants", required=True)
    parser.add_argument("-r", "--mutant_fitness", default=1, type=float)
    arguments = parser.parse_args()
    if not math.isfinite(arguments.mutant_fitness) or arguments.mutant_fitness <= 0:
        parser.error("Mutant fitness must be a positive finite number.")

    start_time = time.perf_counter()
    graph = load_graph(arguments.edges, arguments.mutants, normalize=True)
    result = solve(graph, mutant_fitness=arguments.mutant_fitness)

    print(f"Fixation probability: {result.fixation_probability}")
    print(f"Conditional fixation time: {result.fixation_time}")
    print(f"Absorption time: {result.absorption_time}")
    print(f"Execution time: {time.perf_counter() - start_time} seconds")


if __name__ == "__main__":
    main()
