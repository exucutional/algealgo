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
            res[i][j] = (m1[i][j]+m2[i][j])%2

    return res


def sub(m1, m2):
    res = []
    for i in range(len(m1)):
        res.append([0]*len(m1[0]))
        for j in range(len(res[0])):
            res[i][j] = (m1[i][j]-m2[i][j])%2

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
            
            res[i][j] %= 2
    
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


def mul(m1, m2):
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

    return res

# Only for triangular matrices!
def invert(m):
    res = []
    dim = len(m)
    if dim == 1:
        return [[1]]

    subdim = int(dim/2)
    m_11 = slice(m, 0, subdim, 0, subdim)
    m_11_inv = invert(m_11)
    m_12 = slice(m, 0, subdim, subdim, dim)
    m_22 = slice(m, subdim, dim, subdim, dim)
    m_22_inv = invert(m_22)
    m_11_inv_m_12_m_22_inv = mul(m_11_inv, mul(m_12, m_22_inv))
    for i in range(len(m_11_inv)):
        res.append(m_11_inv[i])
        for j in range(len(m_11_inv_m_12_m_22_inv)):
            res[-1].append(-m_11_inv_m_12_m_22_inv[i][j])
    
    for i in range(len(m_22_inv)):
        res.append([0]*subdim+m_22_inv[i])

    return res



def transpose(m):
    t = []
    for i in range(len(m[0])):
        t.append([0]*len(m))
        for j in range(len(m)):
            t[i][j] = m[j][i]

    return t


def get_E(U_1):
    E = []
    for i in range(len(U_1)):
        E.append(U_1[i][:len(U_1)])
        for j in range(i):
            E[i][j] = 0

    return E



def get_F(D):
    F = []
    for i in range(len(D)):
        F.append(D[i][:len(D)])

    return F


def get_D(C, P_1):
    return mul(C, transpose(P_1))


def get_G(D, FE_inv, U_1):
    return sub(D, mul(FE_inv, U_1))


def get_FE_inv(F, E):
    return mul(F, invert(E))


def get_H(U_1, P_3):
    return mul(U_1, transpose(P_3))


def get_P_3(P_2, subm):
    P_3 = []
    for i in range(subm):
        P_3.append([0]*(subm+len(P_2)))
        P_3[-1][i] = 1

    for i in range(len(P_2)):
        P_3.append([0]*subm+P_2[i][:])

    return P_3


def get_P(P_1, P_3):
    return mul(P_3, P_1)


def get_U(H, U_2):
    U = []
    for i in range(len(H)):
        U.append(H[i][:])

    for i in range(len(U_2)):
        U.append([0]*len(U_2)+U_2[i][:])

    return U


def get_L(L1, L2, FE_inv):
    L = []
    for i in range(len(L1)):
        L.append(L1[i][:]+[0]*len(FE_inv))

    for i in range(len(FE_inv)):
        L.append(FE_inv[i][:]+L2[i][:])

    return L


def get_permutation(p, i, j):
    m = []
    for k in range(p):
        m.append([0]*p)
        if k == i:
            m[-1][j] = 1
        elif k == j:
            m[-1][i] = 1
        else:
            m[-1][k] = 1

    return m

def LUP(A, m, p):
    if m == 1:
        L = [[1]]
        perm_index = 0
        for i in range(p):
            if A[0][i] != 0:
                perm_index = i
                break
        P = get_permutation(p, 0, perm_index)
        U = A[0][:]
        U[0] = A[0][perm_index]
        U[perm_index] = A[0][0]
        return L, [U], P

    subm = int(m/2)
    B = A[:subm]
    C = A[subm:]
    L_1, U_1, P_1 = LUP(B, subm, p)
    D = get_D(C, P_1)
    E = get_E(U_1)
    F = get_F(D)
    FE_inv = get_FE_inv(F, E)
    G = get_G(D, FE_inv, U_1)
    L_2, U_2, P_2 = LUP(slice(G, 0, len(G), subm, p), subm, p-subm)
    P_3 = get_P_3(P_2, subm)
    H = get_H(U_1, P_3)
    P = get_P(P_1, P_3)
    U = get_U(H, U_2)
    L = get_L(L_1, L_2, FE_inv)
    return L, U, P


def read_input():
    m = [[int(i) for i in input().split()]]
    for _ in range(len(m[0])-1):
        m.append([int(i) for i in input().split()])

    return m


def solve():
    inputm = read_input()
    n = max(len(inputm), len(inputm[0]))
    matrix = expand(inputm, n)
    L, U, P = LUP(matrix, len(matrix), len(matrix))
    print_matrix(L, len(inputm))
    print_matrix(U, len(inputm))
    print_matrix(P, len(inputm))


solve()
