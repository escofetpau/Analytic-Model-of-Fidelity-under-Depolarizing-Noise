import itertools
import scipy.linalg as la
import numpy as np

def mitigate(circ, counts, backend, time=None):
    measured_qubits = []
    for gate in circ.data:
        if gate.operation.name == 'measure':
            measured_qubits.append(gate.qubits[0])

    calibrations = backend.properties(datetime=time).to_dict()['qubits']

    readout_error = []
    for qubit in measured_qubits:
        m0p1 = 0
        m1p0 = 0
        for error in calibrations[circ.find_bit(qubit).index]:
            if error['name'] == 'prob_meas0_prep1':
                m0p1 = error['value']
            elif error['name'] == 'prob_meas1_prep0':
                m1p0 = error['value']
        readout_error.append([(1-m1p0, m1p0), (1-m0p1, m0p1)])

    M = []

    # Loop through all possible real value combinations for the qubits (0 and 1)
    for real_values in itertools.product([0, 1], repeat=len(measured_qubits)):
        M.append([])
        
        # Calculate the probability of measuring each combination of measured values
        for measured_values in itertools.product([0, 1], repeat=len(measured_qubits)):
            probability = 1.0
            for qubit_index in range(len(measured_qubits)):
                real_value = real_values[qubit_index]
                measured_value = measured_values[qubit_index]
                probability *= readout_error[qubit_index][real_value][0 if real_value == measured_value else 1]
            
            M[-1].append(probability)

    Minv = la.pinv(M)
    
    # fill missing counts
    for real_values in itertools.product([0, 1], repeat=len(measured_qubits)):
        value_str = ''.join([str(v) for v in real_values])
        if value_str not in counts:
            counts[value_str] = 0
    
    counts_list = [counts[key] for key in sorted(counts.keys())]

    mitigated_list = np.dot(Minv, counts_list)
    mitigated_counts = {key: mitigated_list[i] for i, key in enumerate(sorted(counts.keys()))}

    return mitigated_counts
