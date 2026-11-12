import random
import unittest

import networkx as nx

import numerical_solver
import simple_simulation


def make_graph(graph, mutants):
    for node in graph:
        graph.nodes[node]["state"] = (
            "mutant" if node in mutants else "resident"
        )
    graph.graph["numOfMutants"] = len(mutants)
    return graph


class SimulationTests(unittest.TestCase):
    def test_simulation_matches_exact_solver_on_small_path(self):
        graph = make_graph(nx.path_graph(3), [0])
        expected = numerical_solver.main(graph, mutant_fitness=1.0)

        random.seed(12345)
        actual = simple_simulation.simulation_from_mutants(
            graph,
            mutant_fitness=1.0,
            num_simulations=5000,
        )

        self.assertAlmostEqual(actual[0], expected[0], delta=0.03)
        self.assertAlmostEqual(actual[1], expected[2], delta=0.25)
        self.assertAlmostEqual(actual[2], expected[1], delta=0.35)

    def test_simulation_reflects_advantageous_mutants(self):
        graph = make_graph(nx.path_graph(3), [0])
        neutral = numerical_solver.main(graph, mutant_fitness=1.0)[0]
        expected = numerical_solver.main(graph, mutant_fitness=2.0)[0]

        random.seed(67890)
        actual = simple_simulation.simulation_from_mutants(
            graph,
            mutant_fitness=2.0,
            num_simulations=5000,
        )[0]

        self.assertGreater(expected, neutral)
        self.assertAlmostEqual(actual, expected, delta=0.03)


if __name__ == "__main__":
    unittest.main()
