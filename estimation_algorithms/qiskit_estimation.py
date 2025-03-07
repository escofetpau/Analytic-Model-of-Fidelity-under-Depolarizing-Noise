from qiskit_aer import noise, AerSimulator
from qiskit.quantum_info import state_fidelity
from qiskit.converters import circuit_to_dag, dag_to_circuit
import numpy as np


def qiskit_fidelity(circ, backend, method='density_matrix', time=None, noise_model=None):
    sim_circ = _remove_idle_wires(circ)
    sim_circ = _remove_meas_add_density(sim_circ)

    simulator = AerSimulator(method=method)
    if noise_model is None:
        noise_model = noise.NoiseModel().from_backend(backend, thermal_relaxation=False)

    # noiseless simulation
    result = simulator.run(sim_circ).result()
    state_noiseless = result.data(0)['density_matrix']

    # noisy simulation
    result = simulator.run(sim_circ, noise_model=noise_model).result()
    state_noisy = result.data(0)['density_matrix']

    return state_fidelity(state_noiseless, state_noisy)

def qiskit_fidelity_thermal(circ, backend, method='density_matrix', time=None, error_params=None, gate_times=None, t1_times=None, t2_times=None, noise_model=None):
    if error_params is None:
        error_params, gate_times, t1_times, t2_times = _backend_to_errors(backend, time=time)
    dag = circuit_to_dag(circ)
    layers = [dag_to_circuit(layer['graph']) for layer in dag.layers()]
    measured_qubits = set()

    exec_time = 0
    for layer in layers:
        slowest_gate = 0
        for gate in layer:
            gate_name = f'{gate.name}{circ.find_bit(gate.qubits[0]).index}' + (f'_{circ.find_bit(gate.qubits[1]).index}' if gate.operation.num_qubits == 2 else '')

            if 'measure' in gate_name:
                measured_qubits.add(circ.find_bit(gate.qubits[0]).index)
                continue

            if gate_name in gate_times:
                slowest_gate = max(slowest_gate, gate_times[gate_name])

        exec_time += slowest_gate
        
    sim_circ = _remove_idle_wires(circ)
    sim_circ = _remove_meas_add_density(sim_circ)

    simulator = AerSimulator(method=method)
    if noise_model is None:
        noise_model = noise.NoiseModel().from_backend(backend, thermal_relaxation=False)

    # noiseless simulation
    result = simulator.run(sim_circ).result()
    state_noiseless = result.data(0)['density_matrix']

    # noisy simulation
    result = simulator.run(sim_circ, noise_model=noise_model).result()
    state_noisy = result.data(0)['density_matrix']

    fid = state_fidelity(state_noiseless, state_noisy)

    for i in range(len(measured_qubits)):
        fid *= np.exp(-exec_time/t1_times[i]) * (0.5 * np.exp(-exec_time/t2_times[i]) + 0.5)

    return fid

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

def _backend_to_errors(backend, time=None):
    error_params = {}
    gate_times = {}

    t1_times = []
    t2_times = []

    properties = backend.properties(datetime=time)

    for gate in properties.gates:
        for param in gate.parameters:
            if param.name == 'gate_error':
                error_params[gate.name] = 1-param.value

            elif param.name == 'gate_length':
                gate_times[gate.name] = param.value * 1e-9

    for qubit in properties.qubits:
        for param in qubit:
            if param.name == 'T1':
                t1_times.append(param.value * 1e-6)
            elif param.name == 'T2':
                t2_times.append(param.value * 1e-6)

    return error_params, gate_times, t1_times, t2_times