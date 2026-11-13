import matplotlib.pyplot as plt
import networkx as nx


def init_visualization(graph):
    plt.ion()
    figure, axis = plt.subplots(figsize=(7, 7))
    position = nx.spring_layout(graph, seed=42)
    return {"fig": figure, "ax": axis, "pos": position}


def update_visualization(graph, visualization, visualize, chosen_node=None):
    if not visualize or visualization is None:
        return

    axis = visualization["ax"]
    position = visualization["pos"]

    axis.clear()
    colors = [
        "red" if graph.nodes[node]["state"] == "mutant" else "blue"
        for node in graph.nodes()
    ]
    node_sizes = [
        700 if node == chosen_node else 300
        for node in graph.nodes()
    ]

    nx.draw_networkx_nodes(
        graph,
        position,
        node_color=colors,
        node_size=node_sizes,
        ax=axis,
    )
    nx.draw_networkx_edges(graph, position, alpha=0.5, ax=axis)
    nx.draw_networkx_labels(graph, position, ax=axis)

    axis.set_title(
        f"Mutants: {graph.graph['numOfMutants']} / "
        f"{graph.number_of_nodes()}"
    )
    axis.axis("off")

    plt.draw()
    plt.pause(0.5)
