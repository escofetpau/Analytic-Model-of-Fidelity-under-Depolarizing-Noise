import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT, QuantumVolume, CDKMRippleCarryAdder, DraperQFTAdder

import csv

from estimation_algorithms.depolarizing_estimation import depolarizing_from_errors_dict

step = 0.995

sizes = np.arange(100, 1000, 10)
sizes = np.arange(10, 251, 4)

two_qubit_gates = ['cx', 'cz']
single_qubit_gates = ['id', 'u1', 'u2', 'u3', 'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg']

simulator = AerSimulator()

p1 = [0, 1e-7, 1e-6]

# Save data to CSV
with open(f'link_feasibility_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(list(sizes))
    writer.writerow(p1)

    ##### QFT
    print('QFT')
    qft_l = [[-1 for _ in sizes] for _ in p1]
    for j,p in enumerate(p1):
        l = 0.01
        for i,q in enumerate(sizes):
            circ = QFT(q)
            circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

            while True:
                depolarizing_params = {gate:l for gate in two_qubit_gates} | {gate:p for gate in single_qubit_gates}

                fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=q) # lower bound on the fidelity

                if fid >= 0.99:
                    print(f'QFT {q} qubits: {l} \t| p={p}')
                    qft_l[j][i] = l
                    break
                l *= step

                if l < p:
                    qft_l[j][i] = -1
                    break
    for qft in qft_l:
        writer.writerow(qft)

    ##### QVolume
    print('QVolume')
    qvol_l = [[-1 for _ in sizes] for _ in p1]
    for j,p in enumerate(p1):
        l = 0.01
        for i,q in enumerate(sizes):
            circ = QuantumVolume(q)
            circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

            while True:
                depolarizing_params = {gate:l for gate in two_qubit_gates} | {gate:p for gate in single_qubit_gates}

                fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=q) # lower bound on the fidelity

                if fid >= 0.99:
                    print(f'QVol {q} qubits: {l} \t| p={p}')
                    qvol_l[j][i] = l
                    break
                l *= step

                if l < p:
                    qvol_l[j][i] = -1
                    break
    for qvol in qvol_l:
        writer.writerow(qvol)


    ##### CDKM Ripple Carry Adder
    print('CDKM Ripple Carry Adder')
    cdkm_l = [[-1 for _ in sizes] for _ in p1]
    for j,p in enumerate(p1):
        l = 0.01
        for i,q in enumerate(sizes):
            circ = QuantumCircuit(q)
            adder = CDKMRippleCarryAdder(int(q/2)-1)
            circ.compose(adder, inplace=True)
            circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

            while True:
                depolarizing_params = {gate:l for gate in two_qubit_gates} | {gate:p for gate in single_qubit_gates}

                fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=q)

                if fid >= 0.99:
                    print(f'CDKM {q} qubits: {l} \t| p={p}')
                    cdkm_l[j][i] = l
                    break
                l *= step

                if l < p:
                    cdkm_l[j][i] = -1
                    break
    for cdkm in cdkm_l:
        writer.writerow(cdkm)


    ##### Draper QFT Adder
    print('Draper QFT Adder')
    draper_l = [[-1 for _ in sizes] for _ in p1]
    for j,p in enumerate(p1):
        l = 0.01
        for i,q in enumerate(sizes):
            circ = QuantumCircuit(q)
            adder = DraperQFTAdder(int(q/2)-1)
            circ.compose(adder, inplace=True)
            circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

            while True:
                depolarizing_params = {gate:l for gate in two_qubit_gates} | {gate:p for gate in single_qubit_gates}

                fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=q)

                if fid >= 0.99:
                    print(f'Draper {q} qubits: {l} \t| p={p}')
                    draper_l[j][i] = l
                    break
                l *= step

                if l < p:
                    draper_l[j][i] = -1
                    break
    for draper in draper_l:
        writer.writerow(draper)


    ##### GHZ
    print('GHZ')
    ghz_l = [[-1 for _ in sizes] for _ in p1]
    for j,p in enumerate(p1):
        l = 0.1
        for i,q in enumerate(sizes):
            circ = QuantumCircuit(q)
            circ.h(0)
            for k in range(1, q):
                circ.cx(0, k)
            circ = transpile(circ, basis_gates=single_qubit_gates+two_qubit_gates)

            while True:
                depolarizing_params = {gate:l for gate in two_qubit_gates} | {gate:p for gate in single_qubit_gates}

                fid = depolarizing_from_errors_dict(circ, depolarizing_params, num_qubits=q)

                if fid >= 0.99:
                    print(f'GHZ {q} qubits: {l} \t| p={p}')
                    ghz_l[j][i] = l
                    break
                l *= step

                if l < p:
                    ghz_l[j][i] = -1
                    break
    for ghz in ghz_l:
        writer.writerow(ghz)