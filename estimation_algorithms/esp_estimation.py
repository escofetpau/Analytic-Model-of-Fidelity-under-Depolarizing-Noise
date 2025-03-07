import numpy as np
from qiskit.converters import circuit_to_dag, dag_to_circuit

def esp(circ, backend, time=None, error_params=None, gate_times=None, t1_times=None, t2_times=None):
    if error_params is None:
        error_params, _, _, _ = _backend_to_errors(backend, time=time)

    prob = 1
    for gate in circ:
        if gate.operation.num_qubits == 1:
            if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}' in error_params:
                    prob *= error_params[f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}']
        else:
            if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}' in error_params:
                prob *= error_params[f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}']

    return prob

def esp_thermal(circ, backend, time=None, error_params=None, gate_times=None, t1_times=None, t2_times=None):
    if error_params is None:
        error_params, gate_times, t1_times, t2_times = _backend_to_errors(backend, time=time)

    prob = 1
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

            if gate.operation.num_qubits == 1:
                if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}' in error_params:
                        prob *= error_params[f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}']
            else:
                if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}' in error_params:
                    prob *= error_params[f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}']

        exec_time += slowest_gate

    
    for i in range(len(measured_qubits)):
        prob *= np.exp(-exec_time/t1_times[i]) * (0.5 * np.exp(-exec_time/t2_times[i]) + 0.5)

    return prob

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