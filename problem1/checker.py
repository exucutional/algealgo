from collections import namedtuple, defaultdict
from enum import Enum
from random import randrange

def ceillog2(x):
    k = 0
    t = 1
    while t < x:
        k += 1
        t *= 2
    return k

Circuit = namedtuple('Circuit', ['gates', 'inputs', 'outputs'])
Gate = namedtuple('Gate', ['opcode', 'inputs'])

class CircuitRequirements(Enum):
    STANDARD_BASIS = 0
    NO_UNREACHABLE_GATES = 1
    
    
def read_circuit(s, options={CircuitRequirements.STANDARD_BASIS, CircuitRequirements.NO_UNREACHABLE_GATES}, basis=None):
    gates = dict()
    outputs = dict()

    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        tokens = line.split()
        type_ = tokens[0]
        if type_ == 'GATE':
            gate = Gate(opcode=tokens[2], inputs=list(map(int, tokens[3:])))
            node_number = int(tokens[1])
            if node_number in gates:
                print('Gate at node #{node_number} specified twice')
                return None
            gates[node_number] = gate
            if CircuitRequirements.STANDARD_BASIS in options:
                basis = {'AND': 2, 'OR': 2, 'NOT': 1}
            if basis is not None:
                if gate.opcode not in basis:
                    print(f'Wrong gate opcode: {gate.opcode}')
                    return None
                if len(gate.inputs) != basis[gate.opcode]:
                    print(f'Wrong number of inputs for gate #{node_number}')
                    return None
        elif type_ == 'OUTPUT':
            if len(tokens) > 3:
                print('Wrong output specification')
                return None
            k = int(tokens[1])
            if k in outputs:
                print('Same output #{k} specified twice')
                return None
            outputs[k] = int(tokens[2])
        else:
            print('Wrong file format')
            return None
        

    if sorted(gates) != list(range(min(gates), max(gates) + 1)):
        print('Gate numbers do not form a continuous interval')
        return None
    
    for k in outputs:
        if k > max(gates):
            print(f'Output #{k} is neither a gate nor an input')

    for gate in gates:
        for k in gates[gate].inputs:
            if k > max(gates):
                print(f'Input #{k} of gate #{gate} is invalid')
                return None
    
    if CircuitRequirements.NO_UNREACHABLE_GATES in options:
        reachable_vertices = set()
        def set_as_reachable(node):
            reachable_vertices.add(node)
            if node in gates:
                for k in gates[node].inputs:
                    if k not in reachable_vertices:
                        set_as_reachable(k)
        for output in outputs.values():
            set_as_reachable(output)
        if not set(gates) <= reachable_vertices:
            print('Some gates are not reachable from the output nodes. These should be eliminated from the circuit.')
            return None
            
    def has_reachable_cycles(node):
        dfs_stack = [node]
        dfs_stack_set = {node}
        visited_nodes = set()
        while dfs_stack != []:
            node = dfs_stack[-1]
            visited_nodes.add(node)
            if node in gates:
                for k in gates[node].inputs:
                    if k in dfs_stack_set:
                        return True
                    if k not in visited_nodes:
                        dfs_stack.append(k)
                        dfs_stack_set.add(k)
                        break
                else:
                    dfs_stack_set.remove(dfs_stack.pop())
            else:
                dfs_stack_set.remove(dfs_stack.pop())
        return False
            
    if any(map(has_reachable_cycles, outputs.values())):
        print('A cycle found that is reachable from a circuit output. Cannot evaluate such circuit.')
        return None
    
    inputs = sorted(range(0, min(gates)))
    return Circuit(gates=gates, outputs=outputs, inputs=inputs)


def get_depth(circuit):
    depths = dict()
    def get_depth_at_node(node):
        if node in depths:
            return depths[node]
        if node not in circuit.gates:
            return 0
        depths[node] = 1 + max(map(get_depth_at_node, circuit.gates[node].inputs))
        return depths[node]
    return max(map(get_depth_at_node, circuit.outputs.values()))


def get_size(c):
    return len(c.gates)

def evaluate_circuit(circuit, input_values, is_vectorized=False):
    evaluations = dict()
    for i, v in enumerate(input_values):
        evaluations[i] = v
    
    if is_vectorized:
        operations = {
            'AND': (lambda x,y: x & y), 
            'OR': (lambda x,y: x | y), 
            'NOT': (lambda x: 0xFFFF ^ x)
        }
    else:
        operations = {
            'AND': min, 
            'OR': max, 
            'NOT': (lambda x: 1-x)
        }
    
    def evaluate_at_node(node):
        if node in evaluations:
            return evaluations[node]
        gate = circuit.gates[node]
        evaluations[node] = operations[gate.opcode](*map(evaluate_at_node, gate.inputs))
        return evaluations[node]

    for node in circuit.outputs.values():
        evaluate_at_node(node)
    return evaluations


def check(reply, n):
    circuit = read_circuit(
        reply, options={
            CircuitRequirements.NO_UNREACHABLE_GATES,
        },
        basis={'OR': 2}
    )
    evals = evaluate_circuit(circuit, [0] * n)
    if any(evals[circuit.outputs[i]] != 0 for i in range(n)):
        return False
    
    for k in range(n):
        vals = [0] * n
        vals[k] = 1
        evals = evaluate_circuit(circuit, vals)
        if any(evals[circuit.outputs[i]] != 1 for i in range(k, n)):
            return False
        if any(evals[circuit.outputs[i]] != 0 for i in range(k)):
            return False
    
    opt_size = sum(n - 2**k for k in range(ceillog2(n)))
    return get_depth(circuit) <= ceillog2(n) and get_size(circuit) <= opt_size
