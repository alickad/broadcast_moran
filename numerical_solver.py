import networkx as nx
import graph_generator_graph as gg
import numpy as np
from scipy.sparse import csc_matrix, eye
from scipy.sparse.linalg import spsolve

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
                        new_state = curr | (1 << neighbor)  # make neighbor mutant
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
                    new_state = new_state | (1 << neighbor)  # make neighbor mutant
                transitions.append((state_index[new_state], state_index[state], mutant_fitness))
            else:  # node is resident
                for neighbor in graph.neighbors(node):
                    new_state = state & ~(1 << neighbor)  # make neighbor resident
                transitions.append((state_index[new_state], state_index[state], 1))
    return transitions


#print(find_reachable_states(gg.generate_cycle(6, [0])))  # Example usage

def main(graph):
    ALL_MUTANTS = (1 << graph.number_of_nodes()) - 1
    ALL_RESIDENTS = 0
    NUM_NODES = graph.number_of_nodes()

    reachable_states = sorted(list(find_reachable_states(graph)))
    tmp = reachable_states[1]  # second to last state
    reachable_states[1] = reachable_states[-1]  # last state
    reachable_states[-1] = tmp  # second to last state

    state_index = {}
    for i in range(len(reachable_states)):
        state_index[reachable_states[i]] = i

    raw_transitions = sorted(calculate_transitions(graph, reachable_states))
    transitions = [raw_transitions[0]]
    for i in range(1,len(raw_transitions)):
        if raw_transitions[i][0] == transitions[-1][0] and raw_transitions[i][1] == transitions[-1][1]:
            transitions[-1] = (transitions[-1][0], transitions[-1][1], transitions[-1][2] + raw_transitions[i][2])
        else:
            transitions.append(raw_transitions[i])

    rows_q = []
    cols_q = []
    data_q = []
    rows_r = []
    cols_r = []
    data_r = []

    for transition in transitions:
        row, col, weight = transition
        if weight > 0:
            if col == state_index[ALL_MUTANTS] or col == state_index[ALL_RESIDENTS]:
                rows_r.append(row)
                cols_r.append(col)
                data_r.append(weight)
            else:
                rows_q.append(row)
                cols_q.append(col)
                data_q.append(weight)
    
    R = csr_matrix((data_r, (rows_r, cols_r)), shape=(len(reachable_states) - 2, len(reachable_states) - 2))
    Q = csr_matrix((data_q, (rows_q, cols_q)), shape=(2, 2))