import tempfile
import unittest
from pathlib import Path

from moran.graph_utils import load_graph


class GraphUtilsTests(unittest.TestCase):
    def load_graph_from_text(self, edges, mutants, normalize=False):
        with tempfile.TemporaryDirectory() as directory:
            edge_file = Path(directory) / "edges.in"
            mutant_file = Path(directory) / "mutants.in"
            edge_file.write_text(edges)
            mutant_file.write_text(mutants)
            return load_graph(edge_file, mutant_file, normalize=normalize)

    def test_load_graph_allows_negative_vertex_ids(self):
        graph = self.load_graph_from_text("-5 -2\n-2 10\n", "-5\n")

        self.assertEqual(set(graph.nodes), {-5, -2, 10})
        self.assertEqual(graph.graph["numOfMutants"], 1)

    def test_normalization_remaps_negative_vertex_ids_and_mutants(self):
        graph = self.load_graph_from_text("-5 -2\n-2 10\n", "-5\n", normalize=True)

        self.assertEqual(set(graph.nodes), {0, 1, 2})
        self.assertEqual(graph.nodes[0]["state"], "mutant")
        self.assertEqual(graph.graph["numOfMutants"], 1)

    def test_duplicate_mutants_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate mutants"):
            self.load_graph_from_text("1 2\n", "1\n1\n")

    def test_empty_edge_file_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "edge file is empty"):
            self.load_graph_from_text("", "")


if __name__ == "__main__":
    unittest.main()
