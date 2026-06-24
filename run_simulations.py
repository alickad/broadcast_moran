import argparse
import simple_simulation as sim
import graph_generator_graph as gen
import os
import csv

# CSV - graph type, size, mutant?, total num of vertices?, number of simulations, fixation probility, absorbtion time, fixation time

def simulate(sizeFrom, sizeTo, mutantFitness, numSimulations, graphType):
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
        addToTable(graphType, size, mutantFitness, numSimulations, fixationProbability, stepsTotal, stepsToFixation, mutants, totalVertices)

    
def addToTable(grapthType, size, mutantFitness, numSimulations, fixationProbability, absorptionTime, fixationTime, mutants, totalVertices):
    filename = "simulation_results.csv"
    headers = ["graph type", "size", "mutant fitness", "number of simulations", "fixation probability", "absorbtion time", "fixation time", "mutants", "total vertices"]

    row = [grapthType, size, mutantFitness, numSimulations, fixationProbability, absorptionTime, fixationTime, mutants, totalVertices]

    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as table:
        writer = csv.writer(table)
        writer.writerow(row)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Run simulations for different graph types and sizes.")    

    parser.add_argument(
        "-g",
        "--graphType",
        type=str,
        help=(
            "The type of graph to simulate. Options: 'path', 'cycle', 'path_with_n_leaves'."
        ),
    )
    parser.add_argument(
        "-s",
        "--sizeFrom",
        type=int,  
        help=(
            "The starting size of the graph."
        ),
    )
    parser.add_argument(
        "-t",
        "--sizeTo",
        type=int,
        help=(
            "The ending size of the graph."
        ),
    )
    parser.add_argument(
        "-f",
        "--mutantFitness",
        type=float,
        help=(
            "The fitness of the mutants."
        ),
    )
    parser.add_argument(
        "-n",
        "--numSimulations",
        type=int,
        help=(
            "The number of simulations to run for each graph size."
        ),
    )
    
    args = parser.parse_args()
    simulate(args.sizeFrom, args.sizeTo, args.mutantFitness, args.numSimulations, args.graphType)
