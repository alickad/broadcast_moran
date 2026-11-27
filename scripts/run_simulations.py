import argparse
import csv
from pathlib import Path

from moran import graph_generators as gen
from moran import simulation as sim

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
    sizeFrom,
    sizeTo,
    mutantFitness,
    numSimulations,
    graphType,
    output_file="simulation_results.csv",
):
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
    graphType,
    size,
    mutantFitness,
    numSimulations,
    fixationProbability,
    absorptionTime,
    fixationTime,
    mutants,
    totalVertices,
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
