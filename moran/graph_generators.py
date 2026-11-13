import networkx as nx

from .graph_utils import initialize_graph

# nodes are nubered from left to right
def generate_path(size, mutants):
    path = nx.path_graph(size)
    initialize_graph(path, mutants)

    #nx.draw(path, with_labels=True)
    #plt.show()
    return path

# nodes are numbered "clockwise"
def generate_cycle(size, mutants):
    cycle = nx.cycle_graph(size)
    initialize_graph(cycle, mutants)

    #nx.draw(cycle, with_labels=True)
    #plt.show()
    return cycle


# vertex number 0 is first "non leaf" node, its leaves are 1,2,...,n-1, vertex number n is second "non leaf" node, its leaves are n+1,n+2,...,2n-1 and so on
# size is the length of the "non-leaf" path
# n is the number of leaves for each "non-leaf" node
def generate_path_with_n_leaves(size, n, mutants):
    G = nx.Graph()
    n = n+1

    G.add_nodes_from(range(n))
    for l in range(1, n):
        G.add_edge(l, 0)

    for p in range(1, size):
        G.add_nodes_from(range(p*n, p*n + n))
        for l in range(1, n):
            G.add_edge(p*n, p*n + l)
        G.add_edge(p*n -n, p*n)

    initialize_graph(G, mutants)
    
    #nx.draw(G, with_labels=True)
    #plt.show()
    return G


#generate_path_with_n_leaves(6, 1, [1])
       