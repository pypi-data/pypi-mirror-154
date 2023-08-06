import networkx as nx
import matplotlib.pyplot as plt
import copy
import numpy as np
import itc.graph.generate

# plt.rcParams["figure.figsize"] = (15, 8)


def spring_pos(G):
    return nx.spring_layout(G, weight=None, k=2)


def draw(G, directed=False, weighted=False):
    graph_type = nx.DiGraph() if directed else nx.Graph()
    if itc.graph.generate.is_matrix(G):  # adjacency list
        draw(itc.graph.generate.list_to_matrix(G), directed, weighted)
        return
    G = copy.deepcopy(np.array(G))
    G[G == float("inf")] = 0
    G = nx.from_numpy_matrix(np.array(G), create_using=graph_type)

    plt.clf()
    pos = spring_pos(G)
    nx.draw(G,
            pos=pos,
            node_size=600,
            font_size=16,
            node_color="white",
            edgecolors="black",
            with_labels=True,
            arrowsize=35)
    if weighted:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)
    plt.show()
