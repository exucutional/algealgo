from checker import check

def solve(n):
    res = ""
    gate_n = 3 * n
    outputs = [0 for i in range(2 * n + 2)]

    for i in range(n):
        x = i
        y = n + i
        z = 2 * n + i
        xy = gate_n
        res += f"GATE {gate_n} AND {x} {y}\n"
        gate_n += 1
        xory = gate_n
        res += f"GATE {gate_n} OR {x} {y}\n"
        gate_n += 1
        nxory = gate_n
        res += f"GATE {gate_n} NOT {xory}\n"
        gate_n += 1
        xxnory = gate_n
        res += f"GATE {gate_n} OR {xy} {nxory}\n"
        gate_n += 1
        xxnoryz = gate_n
        res += f"GATE {gate_n} AND {xxnory} {z}\n"
        gate_n += 1
        xxnoryorz = gate_n
        res += f"GATE {gate_n} OR {xxnory} {z}\n"
        gate_n += 1
        nxxnoryorz = gate_n
        res += f"GATE {gate_n} NOT {xxnoryorz}\n"
        gate_n += 1
        xxoryxorz = gate_n
        res += f"GATE {gate_n} OR {xxnoryz} {nxxnoryorz}\n"
        gate_n += 1
        xoryz = gate_n
        res += f"GATE {gate_n} AND {xory} {z}\n"
        gate_n += 1
        carry = gate_n
        res += f"GATE {gate_n} OR {xy} {xoryz}\n"
        gate_n += 1
        outputs[i] = xxoryxorz
        outputs[n+i+2] = carry

    zero = gate_n
    res += f"GATE {gate_n} AND {3 * n + 1} {3 * n + 2}\n"
    gate_n += 1
    outputs[n] = zero
    outputs[n + 1] = zero

    for i in range(len(outputs)):
        res += f"OUTPUT {i} {outputs[i]}\n"

    return res[:-1]


n = int(input())
res = solve(n)
print(res)
check(res, n)