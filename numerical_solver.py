import networkx as nx
import graph_generator_graph as gg

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

#print(find_reachable_states(gg.generate_cycle(6, [0])))  # Example usage
