import unittest

import networkx as nx

from moran import formulas as known_formulas
from moran import exact_solver as numerical_solver


def make_graph(graph, mutants):
    for node in graph:
        graph.nodes[node]["state"] = (
            "mutant" if node in mutants else "resident"
        )
    graph.graph["numOfMutants"] = len(mutants)
    return graph


class NumericalSolverTests(unittest.TestCase):
    def test_all_residents_are_already_absorbed(self):
        result = numerical_solver.main(make_graph(nx.path_graph(3), []))

        self.assertEqual(result, (0.0, 0.0, 0.0))

    def test_all_mutants_are_already_fixed(self):
        result = numerical_solver.main(
            make_graph(nx.path_graph(3), [0, 1, 2])
        )

        self.assertEqual(result, (1.0, 0.0, 0.0))

    def test_two_vertex_graph_with_one_mutant(self):
        fixation_probability, fixation_time, absorption_time = (
            numerical_solver.main(make_graph(nx.path_graph(2), [0]))
        )

        self.assertAlmostEqual(fixation_probability, 0.5)
        self.assertAlmostEqual(fixation_time, 1.0)
        self.assertAlmostEqual(absorption_time, 1.0)

    def test_neutral_cycle_matches_known_fixation_probability(self):
        graph = make_graph(nx.cycle_graph(5), [0])

        fixation_probability = numerical_solver.main(graph, 1.0)[0]

        self.assertAlmostEqual(
            fixation_probability,
            known_formulas.fix_prob_cycle(5, 1.0),
        )

    def test_mutant_fitness_changes_fixation_probability(self):
        graph = make_graph(nx.path_graph(3), [0])

        neutral = numerical_solver.main(graph, 1.0)[0]
        advantageous = numerical_solver.main(graph, 2.0)[0]

        self.assertAlmostEqual(neutral, 1 / 3)
        self.assertGreater(advantageous, neutral)

    def test_subneutral_mutants_have_lower_fixation_probability(self):
        graph = make_graph(nx.path_graph(3), [0])

        neutral = numerical_solver.main(graph, 1.0)[0]
        subneutral = numerical_solver.main(graph, 0.5)[0]

        self.assertAlmostEqual(subneutral, 1 / 7)
        self.assertLess(subneutral, neutral)


if __name__ == "__main__":
    unittest.main()
