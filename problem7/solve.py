def is_quadratic(l, p):
    for i in range(p):
        if (i * i) % p == l:
            return True

    return False


def get_legendre_symbols(p):
    legendre = [i for i in range(p)]
    for l in range(1, p):
        legendre[l] = 1 if is_quadratic(legendre[l], p) else -1

    return legendre

def cyclo_shift(arr):
    shifted = arr[:]
    last = shifted[-1]
    for i in range(1, len(arr)):
        shifted[i] = arr[i - 1]

    shifted[0] = last
    return shifted


def get_adamar_paley(legendre, n):
    adamar = [[1]*n, [1, -1] + legendre]
    for i in range(n-2):
        adamar.append([1] + cyclo_shift(adamar[-1][1:]))

    return adamar


def neg(adamar):
    adamar_neg = []
    for i in range(len(adamar)):
        adamar_neg.append(adamar[i][:])
        for j in range(len(adamar_neg[i])):
            adamar_neg[i][j] *= -1

    return adamar_neg


def get_bch_codes_adamar(adamar):
    codes = []
    for row in adamar:
        codes.append(row[:])
        for i in range(len(codes[-1])):
            codes[-1][i] = 1 if codes[-1][i] == 1 else 0

    return codes


def get_bch_codes(n):
    p = n - 1
    legendre = get_legendre_symbols(p)[1:]
    adamar = get_adamar_paley(legendre, n)
    adamar_neg = neg(adamar)
    return get_bch_codes_adamar(adamar) + get_bch_codes_adamar(adamar_neg)



n = int(input())
codes = get_bch_codes(n)
for code in codes:
    print("".join([str(i) for i in code]))
