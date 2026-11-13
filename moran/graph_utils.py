import networkx as nx


def normalize_vertex_numbers(edges):
    unique_vertices = sorted(
        set(int(vertex) for edge in edges for vertex in edge.split())
    )
    vertex_mapping = {
        old: new for new, old in enumerate(unique_vertices)
    }

    return [
        " ".join(
            str(vertex_mapping[int(vertex)])
            for vertex in edge.split()
        )
        for edge in edges
    ]


def initialize_graph(graph, initial_mutants):
    for node in graph.nodes():
        graph.nodes[node]["state"] = "resident"
    for mutant in initial_mutants:
        graph.nodes[mutant]["state"] = "mutant"
    graph.graph["numOfMutants"] = len(initial_mutants)
    return graph


def create_graph(edges, initial_mutants, normalize=False):
    if normalize:
        edges = normalize_vertex_numbers(edges)
    graph = nx.read_edgelist(edges, nodetype=int)
    return initialize_graph(graph, initial_mutants)


def load_graph(edge_file, mutant_file, normalize=False):
    with open(edge_file) as file:
        edges = file.read().splitlines()
    with open(mutant_file) as file:
        initial_mutants = [int(line) for line in file.read().splitlines()]
    return create_graph(edges, initial_mutants, normalize=normalize)
