import webbrowser

import networkx as nx
import matplotlib.pyplot as plt
import random
from argparse import ArgumentParser
import known_formulas
from pyvis.network import Network
import time

import matplotlib.pyplot as plt

def init_visualization(G):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(7, 7))
    pos = nx.spring_layout(G, seed=42)
    return {"fig": fig, "ax": ax, "pos": pos}

def update_visualization(G, net_dict, visualize, chosen_node=None):
    if not visualize or net_dict is None:
        return
    ax = net_dict["ax"]
    pos = net_dict["pos"]
    
    ax.clear()
    colors = ["red" if G.nodes[node]["state"] == "mutant" else "blue" for node in G.nodes()]
    node_sizes = [700 if node == chosen_node else 300 for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    
    ax.set_title(f"Mutants: {G.graph['numOfMutants']} / {G.number_of_nodes()}")
    ax.axis("off")
    
    plt.draw()
    plt.pause(0.5)  # Pause to render frame live
    

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
    update_visualization(G, None, False, chosen_node)  # Update visualization with the chosen node highlighted
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

    return G, chosen_node

def simulate_spread(G, mutant_fitness, visualize=False, net=None):
    num_of_steps = 0
    while 0 < G.graph['numOfMutants'] < G.number_of_nodes():
        G, chosen_node = moran_broadcast_step(G, mutant_fitness)
        num_of_steps += 1
        if visualize and net:
                update_visualization(G, net, visualize, chosen_node)
                sleep(0.3)

    if G.graph['numOfMutants'] == G.number_of_nodes():
        #print(f"All nodes became mutants in {num_of_steps} steps.")
        return "mutation fixation", num_of_steps
    else:   
        #print(f"All nodes became residents in {num_of_steps} steps.")
        return "mutation extinction", num_of_steps

def simulation_from_mutants(G, mutant_fitness, num_simulations, visualize=False):  
    #nx.draw(G, with_labels=True)
    #plt.show()
    net = None
    if visualize:
        net = init_visualization(G)
        update_visualization(G, net, visualize)
    
    
    steps_total = 0
    steps_to_fixation = 0
    fixations_total = 0
    for i in range(num_simulations):
        G_copy = G.copy()
        result, steps = simulate_spread(G_copy, mutant_fitness, visualize, net)
        steps_total += steps
        if result == "mutation fixation":
            fixations_total += 1
            steps_to_fixation += steps
        #update_visualization(G_copy, net, visualize)
        
    return fixations_total / num_simulations, steps_total / num_simulations, steps_to_fixation / fixations_total if fixations_total > 0 else 0


def main(input_edges, input_mutants, mutant_fitness, num_simulations, visualize=False):
    with open(input_edges, 'r') as f:
        edges = f.read().splitlines()
    with open(input_mutants, 'r') as f:
        initial_mutants = list(map(int, f.read().splitlines()))
    G = create_graph(edges, initial_mutants)

    fixationProbability, stepsTotal, stepsToFixation = simulation_from_mutants(
        G.copy(), 
        mutant_fitness=mutant_fitness, 
        num_simulations=num_simulations, 
        visualize=visualize
        )
    
    print(f"Fixation probability: {fixationProbability}")
    print(f"Absorption time: {stepsTotal}")
    print(f"Conditional fixation time: {stepsToFixation}")

    #print("Theoretical fixation probability:", known_formulas.fix_prob_cycle(G.number_of_nodes(), mutant_fitness))      

    
  



if __name__ == "__main__":   

    parser = ArgumentParser(description="Simulate the spread of a mutation in a graph (broadcast).")

    parser.add_argument(
        "-e",
        "--edges",
        default="examples/edges.in",
        type=str,
        help=(
            "The file with list of edges."
        ),
    )
    parser.add_argument(
        "-m",
        "--mutants",
        default="examples/mutants.in",
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
        default=1,
        type=int,
        help=(
            "The number of simulations to run."
        ),
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help=(
            "Visualize the graph and the spread of the mutation in one run of simulation."
        ),
    )
    start_time = time.perf_counter()
    input_args = parser.parse_args()

    main(input_edges=input_args.edges, input_mutants=input_args.mutants, mutant_fitness=input_args.mutant_fitness, num_simulations=input_args.simulations, visualize=input_args.visualize)
    print(f"Execution time: {time.perf_counter() - start_time} seconds")



