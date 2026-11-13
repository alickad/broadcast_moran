from typing import NamedTuple

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix, eye
from scipy.sparse.linalg import spsolve


class SolverResult(NamedTuple):
    fixation_probability: float
    fixation_time: float
    absorption_time: float


def find_starting_state(graph):
    mutants = [
        node for node, data in graph.nodes(data=True)
        if data["state"] == "mutant"
    ]
    start = 0
    for mutant in mutants:
        start += 1 << mutant
    return start


def find_reachable_states(graph):
    start = find_starting_state(graph)
    visited = {start}
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


def calculate_transitions(
    graph,
    reachable_states,
    state_index,
    mutant_fitness=1.0,
):
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


def main(graph, mutant_fitness=1.0):
    all_mutants = (1 << graph.number_of_nodes()) - 1
    all_residents = 0
    num_nodes = graph.number_of_nodes()
    starting_state = find_starting_state(graph)

    if starting_state == all_mutants:
        return SolverResult(1.0, 0.0, 0.0)
    if starting_state == all_residents:
        return SolverResult(0.0, 0.0, 0.0)

    reachable_states = sorted(find_reachable_states(graph))
    reachable_states[1], reachable_states[-1] = (
        reachable_states[-1],
        reachable_states[1],
    )
    state_index = {
        state: index for index, state in enumerate(reachable_states)
    }

    raw_transitions = sorted(
        calculate_transitions(
            graph,
            reachable_states,
            state_index,
            mutant_fitness,
        )
    )
    transitions = [raw_transitions[0]]
    for transition in raw_transitions[1:]:
        if transition[:2] == transitions[-1][:2]:
            previous = transitions[-1]
            transitions[-1] = (
                previous[0],
                previous[1],
                previous[2] + transition[2],
            )
        else:
            transitions.append(transition)

    for index, (row, col, weight) in enumerate(transitions):
        state = reachable_states[row]
        mutant_count = state.bit_count()
        total_selection_weight = (
            mutant_count * mutant_fitness + num_nodes - mutant_count
        )
        transitions[index] = (
            row,
            col,
            weight / total_selection_weight,
        )

    rows_q = []
    cols_q = []
    data_q = []
    rows_r = []
    cols_r = []
    data_r = []

    for transition in transitions:
        row, col, weight = transition
        if weight > 0:
            if (col != state_index[all_mutants] and col != state_index[all_residents]) and ( row != state_index[all_mutants] and row != state_index[all_residents]):
                rows_q.append(row - 2)  #-2 so that the first two states (all mutants and all residents) are not included in the transition matrix for transient states
                cols_q.append(col - 2)      # transient states
                data_q.append(weight)
            elif row != state_index[all_mutants] and row != state_index[all_residents]:
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
    start_vector[state_index[starting_state] - 2] = 1   

    
    start_idx = state_index[starting_state] - 2

    fixation_probability = float(B[start_idx, state_index[all_mutants]])   # probability of absorption into all mutants starting from the starting state
    extinction_probability = 1.0 - fixation_probability

    steps_to_fixation = float(Na[start_idx]) / fixation_probability if fixation_probability > 0 else 0.0
    steps_to_resident = float(Nb[start_idx]) / extinction_probability if extinction_probability > 0 else 0.0
    steps_total = fixation_probability * steps_to_fixation + extinction_probability * steps_to_resident  # expected number of steps to complete absorption starting from the starting state

    fixation_time = steps_to_fixation 
    absorption_time = steps_total

    return SolverResult(
        fixation_probability,
        fixation_time,
        absorption_time,
    )
