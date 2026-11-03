from argparse import ArgumentParser

import networkx as nx
import graph_generator_graph as gg
import numpy as np
from scipy.sparse import csr_matrix, eye
from scipy.sparse.linalg import spsolve
import time

def create_graph(edges, initial_mutants):
    G = nx.Graph()
    G = nx.read_edgelist(edges, nodetype=int)
    for node in G.nodes():
        G.nodes[node]['state'] = 'resident'
    for mutant in initial_mutants:
        G.nodes[mutant]['state'] = 'mutant'  
    G.graph['numOfMutants'] = len(initial_mutants)

    return G

def find_starting_state(graph):
    mutants = [node for node, data in graph.nodes(data=True) if data['state'] == 'mutant']
    start = 0
    for m in mutants:
        start += (1 << m)
    return start

def find_reachable_states(graph):
    mutants = [node for node, data in graph.nodes(data=True) if data['state'] == 'mutant']
    start = 0
    for m in mutants:
        start += (1 << m)
    # start is a bitmask of the initial state
    visited = set()
    visited.add(start)
    stack = [start]
    while stack:
        curr = stack.pop()
        for node in graph:
            new_state = curr
            if (curr & (1 << node)) > 0:  # node is mutant
                for neighbor in graph.neighbors(node):
                    if (curr & (1 << neighbor)) == 0:  # neighbor is resident
                        new_state = new_state | (1 << neighbor)  # make neighbor mutant
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append(new_state)
            else:  # node is resident
                for neighbor in graph.neighbors(node):
                    if (curr & (1 << neighbor)) > 0:  # neighbor is mutant
                        new_state = curr & ~(1 << neighbor)  # make neighbor resident
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append(new_state)
    return visited

def calculate_transitions(graph, reachable_states, mutant_fitness=1.0):
    transitions = []
    for state in reachable_states:
        for node in graph:
            new_state = state
            if (state & (1 << node)) > 0:  # node is mutant
                for neighbor in graph.neighbors(node):
                    new_state |= (1 << neighbor)  # make neighbor mutant
                transitions.append((state_index[state], state_index[new_state], mutant_fitness))
            else:  # node is resident
                for neighbor in graph.neighbors(node):
                    new_state &= ~(1 << neighbor)  # make neighbor resident
                transitions.append((state_index[state], state_index[new_state], 1))
    return transitions
######## MAYBE APPEND new_state and state in oposite order?


#print(find_reachable_states(gg.generate_cycle(6, [0])))  # Example usage

def main(graph, mutant_fitness=1.0):
    ALL_MUTANTS = (1 << graph.number_of_nodes()) - 1
    ALL_RESIDENTS = 0
    NUM_NODES = graph.number_of_nodes()
    STARTING_STATE = find_starting_state(graph)

    reachable_states = sorted(list(find_reachable_states(graph)))
    tmp = reachable_states[1]  # second to last state
    reachable_states[1] = reachable_states[-1]  # last state
    reachable_states[-1] = tmp  # second to last state

    global state_index
    state_index = {}
    for i in range(len(reachable_states)):
        state_index[reachable_states[i]] = i

    raw_transitions = sorted(calculate_transitions(graph, reachable_states, mutant_fitness))
    transitions = [raw_transitions[0]]
    for i in range(1,len(raw_transitions)):
        # if the current transition has the same source and target as the last one in transitions, combine them
        if raw_transitions[i][0] == transitions[-1][0] and raw_transitions[i][1] == transitions[-1][1]:
            transitions[-1] = (transitions[-1][0], transitions[-1][1], transitions[-1][2] + raw_transitions[i][2])
        else:
            transitions.append(raw_transitions[i])
    for i in range(len(transitions)):
        transitions[i] = (transitions[i][0], transitions[i][1], transitions[i][2] / NUM_NODES)  # normalize by number of nodes

    rows_q = []
    cols_q = []
    data_q = []
    rows_r = []
    cols_r = []
    data_r = []

    for transition in transitions:
        row, col, weight = transition
        if weight > 0:
            if (col != state_index[ALL_MUTANTS] and col != state_index[ALL_RESIDENTS]) and ( row != state_index[ALL_MUTANTS] and row != state_index[ALL_RESIDENTS]):
                rows_q.append(row - 2)  #-2 so that the first two states (all mutants and all residents) are not included in the transition matrix for transient states
                cols_q.append(col - 2)      # transient states
                data_q.append(weight)
            elif row != state_index[ALL_MUTANTS] and row != state_index[ALL_RESIDENTS]:
                rows_r.append(row - 2)  #-2 so that the first two states (all mutants and all residents) are not included as rows in the transition matrix for absorbing states
                cols_r.append(col)    # absorbing states
                data_r.append(weight)
    
    Q = csr_matrix((data_q, (rows_q, cols_q)), shape=(len(reachable_states) - 2, len(reachable_states) - 2)).tocsc()    # transition matrix for transient states
    R = csr_matrix((data_r, (rows_r, cols_r)), shape=(len(reachable_states) - 2, 2)).tocsc()    # transition matrix for absorbing states
    I = eye(len(reachable_states) - 2, format='csc')   # identity matrix for transient states

    B = spsolve(I - Q, R)   # probabilities of absorption into each absorbing state starting from each transient state
    a, b = B[:, 1], B[:, 0]   # a is the probability of absorption into all mutants, b is the probability of absorption into all residents
    Na = spsolve(I-Q, a)   # expected number of steps to complete mutation starting from each transient state
    Nb = spsolve(I-Q, b)   # expected number of steps to complete absorption starting from each transient state

    start_vector = np.zeros(len(reachable_states) - 2)
    start_vector[state_index[STARTING_STATE] - 2] = 1   

    
    start_idx = state_index[STARTING_STATE] - 2

    fixation_probability = float(B[start_idx, state_index[ALL_MUTANTS]])   # probability of absorption into all mutants starting from the starting state
    extinction_probability = 1.0 - fixation_probability

    steps_to_fixation = float(Na[start_idx]) / fixation_probability if fixation_probability > 0 else 0.0
    steps_to_resident = float(Nb[start_idx]) / extinction_probability if extinction_probability > 0 else 0.0
    steps_total = fixation_probability * steps_to_fixation + extinction_probability * steps_to_resident  # expected number of steps to complete absorption starting from the starting state

    return fixation_probability, steps_to_fixation, steps_total
    

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
        "-n",
        "--num_simulations",
        default=1000,
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
            "Whether to visualize the graph."
        ),
    )
    start_time = time.perf_counter()
    input_args = parser.parse_args()

    mutant_fitness = input_args.mutant_fitness
    input_edges = input_args.edges
    input_mutants = input_args.mutants
    with open(input_edges, 'r') as f:
        edges = f.read().splitlines()
    with open(input_mutants, 'r') as f:
        initial_mutants = list(map(int, f.read().splitlines()))
    G = create_graph(edges, initial_mutants)

    fixation_probability, steps_to_fixation, steps_total = main(G, mutant_fitness=1.0)
    print(f"Fixation probability: {fixation_probability}")
    print(f"Expected steps to fixation: {steps_to_fixation}")
    print(f"Expected total steps: {steps_total}")
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time} seconds")