import sys
from collections import defaultdict

def print_matrix(m, n):
    s = ""
    for i in range(n):
        for j in range(n):
            s += f"{m[i][j]} "

        s += "\n"

    print(s[:-1])


def slice(m, r1, r2, c1, c2):
    res = m[r1:r2]
    for i in range(len(res)):
        res[i] = res[i][c1:c2]
    
    return res


def add(m1, m2):
    res = []
    for i in range(len(m1)):
        res.append([0]*len(m1[0]))
        for j in range(len(res[0])):
            res[i][j] = (m1[i][j]+m2[i][j])

    return res


def sub(m1, m2):
    res = []
    for i in range(len(m1)):
        res.append([0]*len(m1[0]))
        for j in range(len(res[0])):
            res[i][j] = (m1[i][j]-m2[i][j])

    return res


def mul_expanded(m1, m2):
    dim = len(m1)
    if dim == 1:
        return [[m1[0][0]*m2[0][0]]]

    subdim = int(dim/2)
    m1_11 = slice(m1, 0, subdim, 0, subdim)
    m1_12 = slice(m1, 0, subdim, subdim, dim)
    m1_21 = slice(m1, subdim, dim, 0, subdim)
    m1_22 = slice(m1, subdim, dim, subdim, dim)
    m2_11 = slice(m2, 0, subdim, 0, subdim)
    m2_12 = slice(m2, 0, subdim, subdim, dim)
    m2_21 = slice(m2, subdim, dim, 0, subdim)
    m2_22 = slice(m2, subdim, dim, subdim, dim)

    d = mul_expanded(add(m1_11, m1_22), add(m2_11, m2_22))
    d1 = mul_expanded(sub(m1_12, m1_22), add(m2_21, m2_22))
    d2 = mul_expanded(sub(m1_21, m1_11), add(m2_11, m2_12))
    h1 = mul_expanded(add(m1_11, m1_12), m2_22)
    h2 = mul_expanded(add(m1_21, m1_22), m2_11)
    v1 = mul_expanded(m1_22, sub(m2_21, m2_11))
    v2 = mul_expanded(m1_11, sub(m2_12, m2_22))
    res = []
    for i in range(dim):
        res.append([0]*dim)
        for j in range(dim):
            subi = i-subdim
            subj = j-subdim
            if i < subdim and j < subdim:
                res[i][j] = d[i][j]+d1[i][j]+v1[i][j]-h1[i][j]
            if i < subdim and not j < subdim:
                res[i][j] = v2[i][subj]+h1[i][subj]
            if not i < subdim and j < subdim:
                res[i][j] = v1[subi][j]+h2[subi][j]
            if not i < subdim and not j < subdim:
                res[i][j] = d[subi][subj]+d2[subi][subj]+v2[subi][subj]-h2[subi][subj]

    return res


def expand(m, n):
    res = [r[:] for r in m]
    while n & (n-1) != 0:
        n += 1
    
    for i in range(len(res)):
        res[i].extend([0]*(n-len(res[i])))

    for _ in range(n-len(res)):
        res.append([0]*n)
        res[-1][len(res)-1] = 1

    return res


def mul(m1, m2, clap_to_1=False):
    m1_m = len(m1)
    m1_p = len(m1[0])
    m2_m = len(m2)
    m2_p = len(m2[0])
    assert(m1_p == m2_m)
    if m1_p == 1 and m1_p == 1:
        return [[i*m1[0][0] for i in m2[0]]]

    n = max(max(len(m1), len(m1[0])), max(len(m2), len(m2[0])))
    m1_expanded = expand(m1, n)
    m2_expanded = expand(m2, n)
    assert(len(m1_expanded) == len(m2_expanded) and len(m1_expanded[0]) == len(m2_expanded[0]))
    expanded_res = mul_expanded(m1_expanded, m2_expanded)
    res = []
    for i in range(m1_m):
        res.append(expanded_res[i][:m2_p])

    if clap_to_1:
        for i in range(len(res)):
            for j in range(len(res[i])):
                if res[i][j] > 0:
                    res[i][j] = 1

    return res


def copy(m):
    return [r[:] for r in m]


def is_full(graph):
    for row in graph:
        for column in row:
            if column == 0:
                return False

    return True


def get_dist_graph(graph):
    graphs = [copy(graph), mul(graph, graph, True)]
    while not is_full(graphs[-1]):
        A = graphs[-1]
        A2 = mul(A, A, True)
        graphs.append(A2)

    for graph in graphs:
        for i in range(len(graph)):
            graph[i][i] = 0
            
    D2 = graphs[-1]
    for i in range(len(graphs)-2, -1, -1):
        A = graphs[i]
        D2_A = mul(D2, A, False)
        D = copy(D2)
        deg = [sum([1 if A_row_col != 0 else 0 for A_row_col in A_row]) for A_row in A]
        for i in range(len(D)):
            for j in range(len(D[i])):
                if D2_A[i][j] >= D2[i][j]*deg[j]:
                    D[i][j] = 2*D[i][j]
                else:
                    D[i][j] = 2*D[i][j]-1

        D2 = D

    return D2


def get_pair_dists(graph):
    dist_graph = get_dist_graph(graph)
    pairs = defaultdict(int)
    for i in range(len(dist_graph)):
        for j in range(i, len(dist_graph)):
            if dist_graph[i][j] != 0:
                pairs[dist_graph[i][j]] += 1

    return sorted(pairs.items())


def read_input():
    vertex_count = 0
    edges = []
    for line in sys.stdin:
        if "\x04" not in line and line != "\n":
            edge = line.strip().split()
            edges.append((int(edge[0]), int(edge[1])))
            vertex_count = max(max(int(edge[0])+1, int(edge[1])+1), vertex_count)
        else:
            break

    graph = [[0]*vertex_count for i in range(vertex_count)]
    for edge in edges:
        graph[edge[0]][edge[1]] = 1
        graph[edge[1]][edge[0]] = 1

    for i in range(vertex_count):
        graph[i][i] = 1

    return graph


graph = read_input()
pair_dists = get_pair_dists(graph)
for (dist, count) in pair_dists:
    print(f"{dist} {count}")
