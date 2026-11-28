import argparse
import csv
from pathlib import Path

from moran import graph_generators as gen
from moran import simulation as sim

"""This script runs simulations for different graph types and sizes, and appends the results to a CSV file. 
The results include fixation probability, absorption time, and conditional fixation time 
for the Moran process on the specified graph type. It is mainly intended for large graphs, where
the computation lasts a long time, and we want to save the results to a file. The results can be later analyzed and plotted using other tools.
Usage:
    python run_simulations.py -g <graph_type> -s <size_from> -t <size_to> -f <mutant_fitness> -n <num_simulations> -o <output_file>
Arguments:
    -g, --graphType: The type of graph to simulate. Choices are "path", "cycle", "path_with_n_leaves".
    -s, --sizeFrom: The starting size of the graph.
    -t, --sizeTo: The ending size of the graph.
    -f, --mutantFitness: The fitness of the mutants.
    -n, --numSimulations: The number of simulations to run for each graph size.
    -o, --output: CSV file to append results to (default: simulation_results.csv).
"""

RESULT_HEADERS = [
    "graph type",
    "size",
    "mutant fitness",
    "number of simulations",
    "fixation probability",
    "absorption time",
    "conditional fixation time",
    "mutants",
    "total vertices",
]


def simulate(
    sizeFrom: int,
    sizeTo: int,
    mutantFitness: float,
    numSimulations: int,
    graphType: str,
    output_file="simulation_results.csv",
):
    """Run simulations for a given graph type and size range. The results are appended to a CSV file."""
    for size in range(sizeFrom, sizeTo + 1):
        match graphType:
            case "path":
                mutants = [0]
                G = gen.generate_path(size, mutants)
                totalVertices = size
            case "cycle":
                mutants = [0]
                G = gen.generate_cycle(size, mutants)
                totalVertices = size
            case "path_with_n_leaves":
                n = 1 # change n if wanted
                mutants = [0]
                G = gen.generate_path_with_n_leaves(size, n, mutants)
                totalVertices = size + size * n
   
        fixationProbability, stepsTotal, stepsToFixation = sim.simulation_from_mutants(G.copy(), mutant_fitness=mutantFitness, num_simulations=numSimulations)
        addToTable(
            graphType,
            size,
            mutantFitness,
            numSimulations,
            fixationProbability,
            stepsTotal,
            stepsToFixation,
            mutants,
            totalVertices,
            output_file,
        )


def addToTable(
    graphType: str,
    size: int,
    mutantFitness: float,
    numSimulations: int,
    fixationProbability: float,
    absorptionTime: float,
    fixationTime: float,
    mutants: list,
    totalVertices: int,
    output_file="simulation_results.csv",
):
    output_path = Path(output_file)
    write_header = not output_path.exists() or output_path.stat().st_size == 0
    row = [
        graphType,
        size,
        mutantFitness,
        numSimulations,
        fixationProbability,
        absorptionTime,
        fixationTime,
        mutants,
        totalVertices,
    ]

    with output_path.open("a", newline="", encoding="utf-8") as table:
        writer = csv.writer(table)
        if write_header:
            writer.writerow(RESULT_HEADERS)
        writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run simulations for different graph types and sizes."
    )

    parser.add_argument(
        "-g",
        "--graphType",
        type=str,
        choices=["path", "cycle", "path_with_n_leaves"],
        required=True,
        help="The type of graph to simulate.",
    )
    parser.add_argument(
        "-s",
        "--sizeFrom",
        type=int,
        required=True,
        help="The starting size of the graph.",
    )
    parser.add_argument(
        "-t",
        "--sizeTo",
        type=int,
        required=True,
        help="The ending size of the graph.",
    )
    parser.add_argument(
        "-f",
        "--mutantFitness",
        type=float,
        required=True,
        help="The fitness of the mutants.",
    )
    parser.add_argument(
        "-n",
        "--numSimulations",
        type=int,
        required=True,
        help="The number of simulations to run for each graph size.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="simulation_results.csv",
        help="CSV file to append results to (default: simulation_results.csv).",
    )

    args = parser.parse_args()
    simulate(
        args.sizeFrom,
        args.sizeTo,
        args.mutantFitness,
        args.numSimulations,
        args.graphType,
        args.output,
    )
