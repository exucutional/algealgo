import random
from time import time


def fast_exp(a, n, size):
    if n == 0:
        return 1
    if n % 2 == 1:
        return int((a*fast_exp(a, n-1, size))%size)

    sqrtexp = fast_exp(a, n/2, size)
    return int((sqrtexp*sqrtexp)%size)


def mod_div(a, b, size):
    b_inv = fast_exp(b, size-2, size)
    return int((a*b_inv)%size)


def is_degenerated(matrix, size):
    #https://e-maxx.ru/algo/linear_systems_gauss
    non_zero_col = 0
    for step in range(len(matrix)):
        for row in range(non_zero_col, len(matrix)):
            if matrix[row][step] != 0:
                tmp = matrix[row]
                matrix[row] = matrix[non_zero_col]
                matrix[non_zero_col] = tmp
                break

        if matrix[non_zero_col][step] == 0:
            continue

        for row in range(non_zero_col+1, len(matrix)):
            div = mod_div(matrix[row][step], matrix[non_zero_col][step], size)
            for col in range(len(matrix)):
                matrix[row][col] = int((matrix[row][col]-div*matrix[non_zero_col][col])%size)

        non_zero_col += 1

    for i in range(len(matrix)-1, -1, -1):
        zero_row = True
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                zero_row = False
                break

        if zero_row:
            return True

    return False


def generate_matrix(matrix, size):
    random.seed(time())
    m = []
    for u in range(len(matrix)):
        m.append(matrix[u][:])
        for v in range(len(matrix)):
            if m[u][v] != 0:
                m[u][v] = random.randint(1, size - 1)

    return m


def perfect_match_exist(matrix):
    n = 10
    size = 9973
    for _ in range(n):
        if not is_degenerated(generate_matrix(matrix, size), size):
            return True
    
    return False


def read_input():
    n_edge = int(input())
    matrix = []
    matrix_size = 0
    for _ in range(n_edge):
        edge = [int(i) for i in input().split()]
        matrix_size = max(matrix_size, max(edge[0]+1, edge[1]+1))
        for _ in range(1+edge[0]-len(matrix)):
             matrix.append([])
        for _ in range(1+edge[1]-len(matrix[edge[0]])):
            matrix[edge[0]].append(0)

        matrix[edge[0]][edge[1]] = 1

    for i in range(matrix_size-len(matrix)):
        matrix.append([])

    for i in range(matrix_size):
        for _ in range(matrix_size-len(matrix[i])):
            matrix[i].append(0)
    
    return matrix


def solve():
    matrix = read_input()
    if (perfect_match_exist(matrix)):
        print("yes")
    else:
        print("no")


solve()
