from time import sleep
from typing import NamedTuple

import networkx as nx
import random

from .visualization import init_visualization, update_visualization


class SimulationResult(NamedTuple):
    fixation_probability: float
    absorption_time: float
    fixation_time: float


def moran_broadcast_step(G, mutant_fitness) -> nx.Graph:
    weights = [
        mutant_fitness if G.nodes[node]["state"] == "mutant" else 1
        for node in G.nodes()
    ]
    chosen_node = random.choices(list(G.nodes()), weights=weights, k=1)[0]
    neighbors = list(G.neighbors(chosen_node))
    if G.nodes[chosen_node]["state"] == "mutant":
        for neighbor in neighbors:
            if G.nodes[neighbor]["state"] == "resident":
                G.nodes[neighbor]["state"] = "mutant"
                G.graph["numOfMutants"] += 1
    else:
        for neighbor in neighbors:
            if G.nodes[neighbor]["state"] == "mutant":
                G.nodes[neighbor]["state"] = "resident"
                G.graph["numOfMutants"] -= 1

    return G, chosen_node


def simulate_spread(G, mutant_fitness, visualize=False, net=None):
    num_of_steps = 0
    while 0 < G.graph["numOfMutants"] < G.number_of_nodes():
        G, chosen_node = moran_broadcast_step(G, mutant_fitness)
        num_of_steps += 1
        if visualize and net:
            update_visualization(G, net, visualize, chosen_node)
            sleep(0.3)

    if G.graph["numOfMutants"] == G.number_of_nodes():
        return "mutation fixation", num_of_steps
    return "mutation extinction", num_of_steps


def simulation_from_mutants(
    G,
    mutant_fitness,
    num_simulations,
    visualize=False,
):
    net = None
    if visualize:
        net = init_visualization(G)
        update_visualization(G, net, visualize)

    steps_total = 0
    steps_to_fixation = 0
    fixations_total = 0
    for _ in range(num_simulations):
        G_copy = G.copy()
        result, steps = simulate_spread(
            G_copy,
            mutant_fitness,
            visualize,
            net,
        )
        steps_total += steps
        if result == "mutation fixation":
            fixations_total += 1
            steps_to_fixation += steps

    return SimulationResult(
        fixations_total / num_simulations,
        steps_total / num_simulations,
        steps_to_fixation / fixations_total if fixations_total > 0 else 0,
    )