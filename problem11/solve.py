import numpy as np
import itertools

def get_matrix(n):
    k = int(np.ceil(np.log2(n)+1))
    cols = 2**(k-1)
    mat = np.zeros((cols, k), dtype=int)
    for col_i in range(cols):
        bincol = bin(col_i)[2:][::-1]
        mat[col_i][0] = 1
        for i in range(1, len(bincol)+1):
            mat[col_i][i] = bincol[i-1]

    return np.transpose(mat)


def check_completeness(clauses, x):
    claus_count = 0
    for clause in clauses:
        res = False
        for x_i in clause:
            if x_i > 0:
                res = res or x[x_i-1]
            else:
                res = res or not x[-x_i-1]

        if res:
            claus_count += 1

    return claus_count



def complete(n, m, matrix, clauses):
    x = np.zeros(n, dtype=int)
    x_res = np.copy(x)
    min_claus_count = len(clauses)*7/8
    max_claus_count = 0
    claus_count = check_completeness(clauses, x)
    if claus_count >= min_claus_count and claus_count > max_claus_count:
        max_claus_count = claus_count
        x_res = np.copy(x)

    for p in range(1, len(matrix)+1):
        x = np.zeros(n, dtype=int)
        for combination in itertools.combinations(matrix, p):
            for i, c_i in enumerate(combination[0]):
                if i < n:
                    x[i] ^= c_i
        
        claus_count = check_completeness(clauses, x)
        if claus_count >= min_claus_count and claus_count > max_claus_count:
            max_claus_count = claus_count
            x_res = np.copy(x)


    return x_res


def completeness(n, m, clauses):
    matrix = get_matrix(n)
    return complete(n, m, matrix, clauses)


def read_input():
    [n, m] = [int(i) for i in input().strip().split()]
    clauses = []
    for _ in range(m):
        clauses.append([int(i) for i in input().strip().split()])

    return n, m, clauses


n, m, clauses = read_input()
answer = completeness(n, m, clauses)
print("".join([str(v) for v in answer]))
