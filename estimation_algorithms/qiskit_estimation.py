from qiskit_aer import noise, AerSimulator
from qiskit.quantum_info import state_fidelity


def qiskit_fidelity(circ, backend, method='density_matrix', time=None):
    sim_circ = _remove_idle_wires(circ)
    sim_circ = _remove_meas_add_density(sim_circ)

    simulator = AerSimulator(method=method)
    noise_model = noise.NoiseModel().from_backend(backend)

    # noiseless simulation
    result = simulator.run(sim_circ).result()
    state_noiseless = result.data(0)['density_matrix']

    # noisy simulation
    result = simulator.run(sim_circ, noise_model=noise_model).result()
    state_noisy = result.data(0)['density_matrix']

    return state_fidelity(state_noiseless, state_noisy)

def qiskit_counts(circ, method='matrix_product_state'):
    simulator = AerSimulator(method=method)

    result = simulator.run(circ, shots=2048).result()
    counts = result.get_counts()

    return counts

def _count_gates(qc):
    gate_count = { qubit: 0 for qubit in qc.qubits }
    for gate in qc.data:
        if gate.operation.name == 'barrier':
            continue
        
        for qubit in gate.qubits:
            gate_count[qubit] += 1
    return gate_count

def _remove_idle_wires(qc):
    qc_out = qc.copy()
    gate_count = _count_gates(qc_out)
    for qubit, count in gate_count.items():
        if count == 0:
            qc_out.qubits.remove(qubit)
    return qc_out

def _remove_meas_add_density(qc):
    qc_out = qc
    to_remove_indices = []
    for i,gate in enumerate(qc_out.data):
        if gate.operation.name == 'measure':
            to_remove_indices.append(i)
    
    for i in reversed(to_remove_indices):
        qc_out.data.pop(i)

    qc_out.save_density_matrix()
    return qc_out