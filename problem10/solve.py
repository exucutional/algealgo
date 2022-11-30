import numpy as np


def cut_density(graph, cut):
    edges_count = 0
    if len(cut)==len(graph):
        return float("inf")

    for v in cut:
        for w in range(len(graph[v])):
            if graph[v][w] == -1 and w not in cut:
                edges_count += 1

    return (edges_count*len(graph))/(len(cut)*(len(graph)-len(cut)))


def minimal_density_cut(graph):
    w, v = np.linalg.eigh(graph)
    eigenvectors = [v[:, i] for i in range(len(v))]
    w_sorted = sorted(w)
    nonzero_w_i = w_sorted.index(w_sorted[1])
    evector = list(eigenvectors[nonzero_w_i])
    evector_sorted = sorted(evector, reverse=True)
    evector_indexes = list(map(lambda x: evector.index(x), evector_sorted))
    minimal_cut = []
    minimal_cut_density = float("inf")
    for i in range(1, len(evector)):
        cut = []
        if i < len(evector)/2:
            cut = evector_indexes[:i]
        else:
            cut = evector_indexes[i:]
        cut_value = cut_density(graph, cut)
        if cut_value < minimal_cut_density:
            minimal_cut_density = cut_value
            minimal_cut = cut
        elif cut_value == minimal_cut_density:
            for i in range(len(minimal_cut)):
                if cut[i] < minimal_cut[i]:
                    minimal_cut = cut
                    break

    return minimal_cut


def read_input():
    edge_count = int(input())
    vertex_count = 0
    edges = []
    for _ in range(edge_count):
        edge = input().strip().split()
        edges.append((int(edge[0]), int(edge[1])))
        vertex_count = max(max(edges[-1][0], edges[-1][1]), vertex_count)

    graph = np.zeros((vertex_count+1, vertex_count+1), dtype=int)
    for edge in edges:
        graph[edge[0]][edge[1]] = -1
        graph[edge[0]][edge[0]] += 1
        graph[edge[1]][edge[0]] = -1
        graph[edge[1]][edge[1]] += 1

    return graph


graph = read_input()
cut = minimal_density_cut(graph)
print(" ".join([str(v) for v in sorted(cut)]))
