from scipy.sparse import dok_matrix
from scipy.optimize import linprog

def vertex_cover(v_weights, e_list):
    e_count = len(e_list)
    v_count = len(v_weights)
    A = dok_matrix((e_count + 2 * v_count, v_count))
    for i in range(e_count):
        A[i, e_list[i][0]] = -1
        A[i, e_list[i][1]] = -1

    for i in range(v_count):
        A[e_count + i, i] = -1
        A[e_count + v_count + i, i] = 1

    b = [-1] * e_count + [0] * v_count + [1] * v_count
    linprog_res = linprog(v_weights, A_ub = A, b_ub = b, bounds=(0, 1), method='interior-point', options={"sparse":True, "tol": 1e-2})
    x_list = linprog_res.x
    covered = [i for i in range(len(v_weights)) if x_list[i] >= 0.5]
    return covered

def read_input():
    v_count = int(input())
    v_weights = []
    for _ in range(v_count):
        v_weights.append(int(input()))

    e_count = int(input())
    e_list = []
    for _ in range(e_count):
        e_list.append([int(e) for e in input().split()])

    return v_weights, e_list


v_weights, e_list = read_input()
cover = vertex_cover(v_weights, e_list)
print(" ".join([str(v) for v in cover]))
