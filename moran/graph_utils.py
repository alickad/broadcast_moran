import networkx as nx


def normalize_vertex_numbers(edges, mutants):
    unique_vertices = sorted(
        set(int(vertex) for edge in edges for vertex in edge.split())
    )
    vertex_mapping = {
        old: new for new, old in enumerate(unique_vertices)
    }

    mutants = [vertex_mapping[mutant] for mutant in mutants]

    return [
        " ".join(
            str(vertex_mapping[int(vertex)])
            for vertex in edge.split()
        )
        for edge in edges
    ], mutants


def initialize_graph(graph, initial_mutants):
    for node in graph.nodes():
        graph.nodes[node]["state"] = "resident"
    for mutant in initial_mutants:
        graph.nodes[mutant]["state"] = "mutant"
    graph.graph["numOfMutants"] = len(initial_mutants)
    return graph


def create_graph(edges, initial_mutants, normalize=False):
    if normalize:
        edges, initial_mutants = normalize_vertex_numbers(edges, initial_mutants)
    graph = nx.read_edgelist(edges, nodetype=int)
    if not nx.is_connected(graph):
        raise ValueError("The graph is not connected. Please provide a connected graph.")
    return initialize_graph(graph, initial_mutants)

def load_graph(edge_file, mutant_file, normalize=False):
    with open(edge_file) as file:
        edges = file.read().splitlines()
        for line in edges:
            if len(line.split()) != 2:
                raise ValueError(
                    f"Invalid edge format: {line}. Each line must contain exactly two vertices."
                )
            if not all(vertex.isdigit() for vertex in line.split()):
                raise ValueError(
                    f"Invalid vertex format: {line}. Vertices must be integers."
                )
    with open(mutant_file) as file:
        initial_mutants = [int(line) for line in file.read().splitlines()]
        for mutant in initial_mutants:
            if mutant not in {int(vertex) for edge in edges for vertex in edge.split()}:
                raise ValueError(
                    f"Mutant {mutant} is not present in the graph defined by the edges."
                )
    return create_graph(edges, initial_mutants, normalize=normalize)
