import networkx as nx
import matplotlib.pyplot as plt
import random
from argparse import ArgumentParser
import known_formulas

def create_graph(edges, initial_mutants):
    G = nx.Graph()
    G = nx.read_edgelist(edges, nodetype=int)
    for node in G.nodes():
        G.nodes[node]['state'] = 'resident'
    for mutant in initial_mutants:
        G.nodes[mutant]['state'] = 'mutant'  
    G.graph['numOfMutants'] = len(initial_mutants)

    return G

def moran_broadcast_step(G, mutant_fitness)->nx.Graph:
    weights = [mutant_fitness if G.nodes[node]['state'] == 'mutant' else 1 for node in G.nodes()]
    chosen_node = random.choices(list(G.nodes()), weights=weights, k=1)[0]
    neighbors = list(G.neighbors(chosen_node))
    if G.nodes[chosen_node]['state'] == 'mutant':
        for neighbor in neighbors:
            if G.nodes[neighbor]['state'] == 'resident':
                G.nodes[neighbor]['state'] = 'mutant'
                G.graph['numOfMutants'] += 1
    else:
        for neighbor in neighbors:
            if G.nodes[neighbor]['state'] == 'mutant':
                G.nodes[neighbor]['state'] = 'resident'
                G.graph['numOfMutants'] -= 1

    return G

def simulate_spread(G, mutant_fitness):
    num_of_steps = 0
    while 0 < G.graph['numOfMutants'] < G.number_of_nodes():
        G = moran_broadcast_step(G, mutant_fitness)
        num_of_steps += 1
    if G.graph['numOfMutants'] == G.number_of_nodes():
        #print(f"All nodes became mutants in {num_of_steps} steps.")
        return "mutation fixation", num_of_steps
    else:   
        #print(f"All nodes became residents in {num_of_steps} steps.")
        return "mutation extinction", num_of_steps

def simulation_from_mutants(G, mutant_fitness, num_simulations):  
    steps_total = 0
    steps_to_fixation = 0
    fixations_total = 0
    for i in range(num_simulations):
        G_copy = G.copy()
        result, steps = simulate_spread(G_copy, mutant_fitness)
        steps_total += steps
        if result == "mutation fixation":
            fixations_total += 1
            steps_to_fixation += steps
    return fixations_total / num_simulations, steps_total / num_simulations, steps_to_fixation / fixations_total if fixations_total > 0 else 0


def main(input_edges, input_mutants, mutant_fitness, num_simulations):
    with open(input_edges, 'r') as f:
        edges = f.read().splitlines()
    with open(input_mutants, 'r') as f:
        initial_mutants = list(map(int, f.read().splitlines()))
    G = create_graph(edges, initial_mutants)

    fixationProbability, stepsTotal, stepsToFixation = simulation_from_mutants(G.copy(), mutant_fitness=mutant_fitness, num_simulations=num_simulations)
    print(f"Fixation probability: {fixationProbability}")
    print(f"Average number of steps: {stepsTotal}")
    print(f"Average fixation time: {stepsToFixation}")

    print("Theoretical fixation probability:", known_formulas.fix_prob_cycle(G.number_of_nodes(), mutant_fitness))      

    
    nx.draw(G, with_labels=True)
    plt.show()



if __name__ == "__main__":   

    parser = ArgumentParser(description="Simulate the spread of a mutation in a graph (broadcast).")

    parser.add_argument(
        "-e",
        "--edges",
        default="inputs/edges.in",
        type=str,
        help=(
            "The file with list of edges."
        ),
    )
    parser.add_argument(
        "-m",
        "--mutants",
        default="inputs/mutants.in",
        type=str,
        help=(
            "The file with list of initial mutants."
        ),
    )
    parser.add_argument(
        "-r",
        "--mutant_fitness",
        default=1,
        type=float,
        help=(
            "The fitness of the mutant."
        ),
    )
    parser.add_argument(
        "-s",
        "--simulations",
        default=10000,
        type=int,
        help=(
            "The number of simulations to run."
        ),
    )
    input_args = parser.parse_args()

    main(input_edges=input_args.edges, input_mutants=input_args.mutants, mutant_fitness=input_args.mutant_fitness, num_simulations=input_args.simulations)



