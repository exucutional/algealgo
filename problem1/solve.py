from collections import deque
from math import ceil, log2

from pkg_resources import ResourceManager
from checker import check

def solve(n):
    res = ""
    outputs = [i for i in range(n)]
    process = deque([i for i in range(n if n % 2 == 0 else n - 1)])
    gate_n = n
    new_levels = []
    left_old = n
    while len(process) > 1:
        left = process.popleft()
        right = process.popleft()
        if right < left:
            tmp = left
            left = right
            right = tmp

        #print(left, right, process)
        outputmin = min(outputs[left], outputs[right])
        outputmax = max(outputs[left], outputs[right])
        res += f"GATE {gate_n} OR {outputmin} {outputmax}\n"
        outputs[right] = gate_n
        if left < left_old:
            new_levels.append(min(left, right))

        left_old = left
        process.append(right)

        gate_n += 1

    new_levels.append(process[0])
    #print(new_levels)

    def subsolve(left, right):
        nonlocal res
        nonlocal gate_n
        if left == right:
            return

        outputmin = min(outputs[left], outputs[right])
        outputmax = max(outputs[left], outputs[right])
        res += f"GATE {gate_n} OR {outputmin} {outputmax}\n"
        outputs[right] = gate_n
        gate_n += 1
        subsolve(left, int((left + right) / 2))
        subsolve(right, right + int((right - left) / 2))

    if n % 2 != 0:
        res += f"GATE {gate_n} OR {n-1} {outputs[n-2]}\n"
        outputs[n - 1] = gate_n
        gate_n += 1

    for i in range(1, len(new_levels) - 1):
        subsolve(new_levels[i], int((new_levels[i + 1] + new_levels[i]) / 2))

    for i in range(len(outputs)):
        res += f"OUTPUT {i} {outputs[i]}\n"

    return res[:-1]


def solve2(n):
    outputs = [i for i in range(n)]
    outputs_next = [i for i in range(n)]
    gate_n = n
    res = ""
    for i in range(ceil(log2(n))):
        for j in range(n):
            #print(i, j, j >= 2**i)
            if j >= 2**i:
                res += f"GATE {gate_n} OR {outputs[j-int(2**i)]} {outputs[j]}\n"
                outputs_next[j] = gate_n
                gate_n += 1
        
        outputs = outputs_next[:]

    for i in range(len(outputs)):
        res += f"OUTPUT {i} {outputs[i]}\n"

    return res[:-1]


n = int(input())
res = solve2(n)
print(res)
#check(res, n)

#for n in range(2, 200):
    #check(solve(n), n)