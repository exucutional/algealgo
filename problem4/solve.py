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
            res[i][j] = (m1[i][j]+m2[i][j])%9

    return res


def sub(m1, m2):
    res = []
    for i in range(len(m1)):
        res.append([0]*len(m1[0]))
        for j in range(len(res[0])):
            res[i][j] = (m1[i][j]-m2[i][j])%9

    return res


def mul(m1, m2):
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

    d = mul(add(m1_11, m1_22), add(m2_11, m2_22))
    d1 = mul(sub(m1_12, m1_22), add(m2_21, m2_22))
    d2 = mul(sub(m1_21, m1_11), add(m2_11, m2_12))
    h1 = mul(add(m1_11, m1_12), m2_22)
    h2 = mul(add(m1_21, m1_22), m2_11)
    v1 = mul(m1_22, sub(m2_21, m2_11))
    v2 = mul(m1_11, sub(m2_12, m2_22))
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
            
            res[i][j] %= 9
    
    return res


def expand(m):
    n = len(m)
    while n & (n-1) != 0:
        n += 1
    
    if n != len(m):
        for i in range(len(m)):
            m[i].extend([0]*(n-len(m)))
        
        for _ in range(n-len(m)):
            m.append([0]*n)


def solve(m):
    n = len(m)
    expand(m)
    res = m
    for i in bin(n)[3:]:
        res = mul(res, res)
        if i == '1':
            res = mul(res, m)
    
    return res


m = [[int(i) for i in input().split()]]
for _ in range(len(m[0])-1):
    m.append([int(i) for i in input().split()])

n = len(m)
res = solve(m)
string = ""
for i in range(n):
    for j in range(n):
        string += f"{res[i][j]} "
    
    string += "\n"

print(string[:-1])
