from estimation_algorithms.depolarizing_estimation import depolarizing_from_errors_dict

from qiskit import QuantumCircuit, transpile

import numpy as np
import csv

two_qubit_gates = ['cx', 'cz']
single_qubit_gates = ['id', 'u1', 'u2', 'u3', 'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg']

circ = QuantumCircuit.from_qasm_file('shor_bench/shor_9_4_indep_qiskit_18.qasm')
circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

p1s = np.linspace(0, 1e-5, 10)
p2s = np.linspace(0, 1e-5, 10)

fidelities = []

for p1 in p1s:
    p1_errors = {gate:p1 for gate in two_qubit_gates}
    fidelities.append([])
    for p2 in p2s:
        depolarizing_params = p1_errors | {gate:p2 for gate in single_qubit_gates}

        fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=18)
        print(f'p1={p1} p2={p2} | Fidelity={fid}')
        fidelities[-1].append(fid)

with open('shor_computation_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(p1s)
    writer.writerow(p2s)
    for f in fidelities:
        writer.writerow(f)