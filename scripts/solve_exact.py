import argparse
import time

from moran.graph_utils import load_graph
from moran.exact_solver import main as solve


def main():
    parser = argparse.ArgumentParser(
        description="Solve the broadcast Moran process exactly."
    )
    parser.add_argument("-e", "--edges", default="examples/edges.in")
    parser.add_argument("-m", "--mutants", default="examples/mutants.in")
    parser.add_argument("-r", "--mutant_fitness", default=1, type=float)
    arguments = parser.parse_args()

    start_time = time.perf_counter()
    graph = load_graph(arguments.edges, arguments.mutants, normalize=True)
    result = solve(graph, mutant_fitness=arguments.mutant_fitness)

    print(f"Fixation probability: {result.fixation_probability}")
    print(f"Conditional fixation time: {result.fixation_time}")
    print(f"Absorption time: {result.absorption_time}")
    print(f"Execution time: {time.perf_counter() - start_time} seconds")


if __name__ == "__main__":
    main()
