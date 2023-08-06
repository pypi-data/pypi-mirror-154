import networkx as nx
import random
import itertools
import numpy as np


def to_nx(G):
    if is_matrix(G):
        G = list_to_matrix(G)
    G = np.array(G)
    G[G == float("inf")] = 0
    return nx.from_numpy_matrix(G)


def is_matrix(G):
    return all(map(lambda l: len(l) != len(G), G))


def matrix_empty(n, weighted=False):
    return [[float("inf") if weighted else 0] * n for _ in range(n)]


def matrix_to_list(G):
    pass


def list_to_matrix(G, weighted=False):
    n = len(G)
    M = matrix_empty(n, weighted=weighted)
    for i in range(n):
        for j in G[i]:
            if type(j) is tuple:
                M[i][j[0]] = j[1]
            else:
                M[i][j] = 1
    return M


def random_nx(n=8, p=0.35, directed=False):
    return nx.fast_gnp_random_graph(n, p, directed=directed)


def random_matrix(n=8, p=0.35, directed=False, weighted=False):
    return list_to_matrix(random_list(n, p, directed, weighted), weighted)


def random_list(n=8, p=0.35, directed=False, weighted=False):
    G = [[] for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if random.random() < p:
            G[i].append((j, random.randrange(1, 10)) if weighted else j)
            if not directed:
                G[j].append((i, G[i][-1][1]) if weighted else i)
        if directed and random.random() < p:
            G[j].append((i, random.randrange(1, 10)) if weighted else i)
    return G
