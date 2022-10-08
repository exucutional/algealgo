from itertools import combinations

def binary(num, length=8):
    return format(num, '#0{}b'.format(length + 2))

def calc_val(bit_pos, l, n):
    val = 1 << bit_pos
    offset = 2**l
    for i in range(n-l):
        val = val << offset + val
        offset *= 2

    return val


def calc_single_val(pos, n):
    val = 0
    for i in range(2**n-1, -1, -1):
        bins = binary(i, n)
        bit = int(bins[2:][pos])
        val = (val << 1) + bit
 
    return val


def solve(n):
    res = ""
    gate_n = n
    output_n = 0

    used = set()
    con_num = dict()
    num_gate = dict()
    con_gate = dict()

    for i in range(n):
        num = calc_single_val(i, n)
        res += f"OUTPUT {output_n} {i}\n"
        used.add(num)
        con_num[frozenset([i])] = num
        num_gate[num] = i
        con_gate[frozenset([i])] = i
        output_n += 1

    for i in range(n):
        res += f"GATE {gate_n} NOT {i}\n"
        num = ~calc_single_val(i, n)&(2**(2**n)-1)
        used.add(num) 
        res += f"OUTPUT {output_n} {gate_n}\n"
        con_num[frozenset([n+i])] = num
        num_gate[num] = gate_n
        con_gate[frozenset([n+i])] = gate_n
        gate_n += 1
        output_n += 1

    for i in range(2, n+1):
        for c in combinations([i for i in range(2*n)], i):
            num = ~0
            for c_i in c:
                num &= con_num[frozenset([c_i])]

            con_num[frozenset(c)] = num
            and1 = 0
            and2 = 0
            for c_i in combinations(c, i-1):
                if frozenset(c_i) in con_gate:
                    and1 = con_gate[frozenset(c_i)]
                    and2 = con_gate[frozenset(set(c).difference(set(c_i)))]
                    break

            if num not in used:
                used.add(num)
                res += f"GATE {gate_n} AND {and1} {and2}\n"
                res += f"OUTPUT {output_n} {gate_n}\n"
                con_gate[frozenset(c)] = gate_n
                num_gate[num] = gate_n
                output_n += 1
                gate_n += 1




    numgates = {}
    for i in range(2**n):
        numgates[1 << i] = num_gate[1 << i]

    nums1 = list(numgates.keys())
    nums = nums1[:]
    for i in range(2, 2**n + 1):
        new_nums = []
        for num1 in nums1:
            for num in nums:
                newnum = num1 | num
                if num1 != num and newnum not in used:
                    used.add(newnum)
                    res += f"GATE {gate_n} OR {numgates[num1]} {numgates[num]}\n"
                    res += f"OUTPUT {output_n} {gate_n}\n"
                    numgates[newnum] = gate_n
                    new_nums.append(newnum)
                    gate_n += 1
                    output_n += 1
        
        nums = new_nums[:]
    
    if 0 not in num_gate:
        res += f"GATE {gate_n} NOT {gate_n-1}\n"
        res += f"OUTPUT {output_n} {gate_n}\n"

    return res[:-1]


n = int(input())
res = solve(n)
print(res)