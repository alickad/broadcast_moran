import networkx as nx
import matplotlib.pyplot as plt
import random

def create_graph(edges, initial_mutants):
    G = nx.Graph()
    G = nx.read_edgelist(edges, nodetype=int)
    for node in G.nodes():
        G.nodes[node]['state'] = 'resident'
    for mutant in initial_mutants:
        G.nodes[mutant]['state'] = 'mutant'  
    G.graph['numOfMutants'] = len(initial_mutants)

    return G

def moran_broadcast_step(G, mutant_fitness):
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
        print(f"All nodes became mutants in {num_of_steps} steps.")
        return "mutation fixation", num_of_steps
    else:   
        print(f"All nodes became residents in {num_of_steps} steps.")
        return "mutation extinction", num_of_steps

def simulation_from_mutants(G, mutant_fitness, num_simulations):  
    steps_total = 0
    fixations_total = 0
    for i in range(num_simulations):
        G_copy = G.copy()
        result, steps = simulate_spread(G_copy, mutant_fitness)
        steps_total += steps
        if result == "mutation fixation":
            fixations_total += 1
    print(f"Fixation probability: {fixations_total / num_simulations:.4f}")
    print(f"Average steps to fixation/extinction: {steps_total / num_simulations:.2f}")   


def main():
    input_edges = "edges.txt"  
    input_mutants = "mutants.txt"
    with open(input_edges, 'r') as f:
        edges = f.read().splitlines()
    with open(input_mutants, 'r') as f:
        initial_mutants = list(map(int, f.read().splitlines()))
    G = create_graph(edges, initial_mutants)

    simulation_from_mutants(G.copy(), mutant_fitness=1.0, num_simulations=5000)
    
    nx.draw(G, with_labels=True)
    plt.show()



if __name__ == "__main__":    main()    

