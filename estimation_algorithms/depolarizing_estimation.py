import numpy as np
from qiskit.converters import circuit_to_dag, dag_to_circuit

def depolarizing(circ, backend, p=0, time=None, error_params=None, gate_times=None, t1_times=None, t2_times=None):
    if error_params is None:
        error_params, gate_times, _, _ = _backend_to_errors(backend, time=time)

    qubits_fidelity = [1.0 for _ in backend.properties().qubits]

    dag = circuit_to_dag(circ)
    layers = [dag_to_circuit(layer['graph']) for layer in dag.layers()]
    measured_qubits = set()

    exec_time = [0]
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
                    qubit = circ.find_bit(gate.qubits[0]).index

                    l = error_params[f'{gate.operation.name}{qubit}']

                    qubits_fidelity[qubit] = (1-l) * qubits_fidelity[qubit] + (1-p) * l/2
            
            else:
                if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}' in error_params:
                    qubit_1 = circ.find_bit(gate.qubits[0]).index
                    qubit_2 = circ.find_bit(gate.qubits[1]).index

                    fid_1 = qubits_fidelity[qubit_1]
                    fid_2 = qubits_fidelity[qubit_2]

                    l = error_params[f'{gate.operation.name}{qubit_1}_{qubit_2}']

                    c = 1/2 *(np.sqrt((1-l) * (fid_1 + fid_2)**2 + l) - np.sqrt(1-l) * (fid_1 + fid_2))

                    fid_1 = np.sqrt(1-l) * fid_1 + (1-p) * c
                    fid_2 = np.sqrt(1-l) * fid_2 + (1-p) * c

                    qubits_fidelity[qubit_1] = fid_1
                    qubits_fidelity[qubit_2] = fid_2

        exec_time.append(exec_time[-1] + slowest_gate)

    return np.prod(qubits_fidelity)

def depolarizing_thermal(circ, backend, p=0, time=None, error_params=None, gate_times=None, t1_times=None, t2_times=None):
    if error_params is None:
        error_params, gate_times, t1_times, t2_times = _backend_to_errors(backend, time=time)

    qubits_fidelity = [1.0 for _ in backend.properties().qubits]

    dag = circuit_to_dag(circ)
    layers = [dag_to_circuit(layer['graph']) for layer in dag.layers()]
    measured_qubits = set()

    exec_time = [0]
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
                    qubit = circ.find_bit(gate.qubits[0]).index

                    l = error_params[f'{gate.operation.name}{qubit}']

                    qubits_fidelity[qubit] = (1-l) * qubits_fidelity[qubit] + (1-p) * l/2
            
            else:
                if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}' in error_params:
                    qubit_1 = circ.find_bit(gate.qubits[0]).index
                    qubit_2 = circ.find_bit(gate.qubits[1]).index

                    fid_1 = qubits_fidelity[qubit_1]
                    fid_2 = qubits_fidelity[qubit_2]

                    l = error_params[f'{gate.operation.name}{qubit_1}_{qubit_2}']

                    c = 1/2 *(np.sqrt((1-l) * (fid_1 + fid_2)**2 + l) - np.sqrt(1-l) * (fid_1 + fid_2))

                    fid_1 = np.sqrt(1-l) * fid_1 + (1-p) * c
                    fid_2 = np.sqrt(1-l) * fid_2 + (1-p) * c

                    qubits_fidelity[qubit_1] = fid_1
                    qubits_fidelity[qubit_2] = fid_2

        exec_time.append(exec_time[-1] + slowest_gate)

        for i in range(len(qubits_fidelity)):
            t1_decay = np.exp(-slowest_gate/t1_times[i])
            t2_decay = 0.5 * np.exp(-slowest_gate/t2_times[i]) + 0.5
            qubits_fidelity[i] = qubits_fidelity[i] * t1_decay * t2_decay
    
    return np.prod([qubits_fidelity[i] for i in measured_qubits])

def depolarizing_from_errors_dict(circ, error_params, num_qubits, p=0):
    qubits_fidelity = [1.0 for _ in range(num_qubits)]

    dag = circuit_to_dag(circ)
    layers = [dag_to_circuit(layer['graph']) for layer in dag.layers()]
    measured_qubits = set()

    for layer in layers:
        for gate in layer:
            gate_name = gate.name

            if 'measure' in gate_name:
                measured_qubits.add(circ.find_bit(gate.qubits[0]).index)
                continue

            entangled = np.random.random() < p

            if gate.operation.num_qubits == 1:
                if gate.operation.name in error_params:
                    qubit = circ.find_bit(gate.qubits[0]).index

                    l = error_params[gate.operation.name]

                    if not entangled:
                        qubits_fidelity[qubit] = (1-l) * qubits_fidelity[qubit] + l/2
                    else:
                        qubits_fidelity[qubit] = (1-l) * qubits_fidelity[qubit]
            
            else:
                if gate.operation.name in error_params:
                    qubit_1 = circ.find_bit(gate.qubits[0]).index
                    qubit_2 = circ.find_bit(gate.qubits[1]).index

                    fid_1 = qubits_fidelity[qubit_1]
                    fid_2 = qubits_fidelity[qubit_2]

                    l = error_params[gate.operation.name]

                    if not entangled:
                        c = 1/2 *(np.sqrt((1-l) * (fid_1 + fid_2)**2 + l) - np.sqrt(1-l) * (fid_1 + fid_2))
                    else:
                        c = 0

                    fid_1 = np.sqrt(1-l) * fid_1 + c
                    fid_2 = np.sqrt(1-l) * fid_2 + c

                    qubits_fidelity[qubit_1] = fid_1
                    qubits_fidelity[qubit_2] = fid_2
    
    return np.prod(qubits_fidelity)

def _backend_to_errors(backend, time=None):
    depol_params = {}
    gate_times = {}

    t1_times = []
    t2_times = []

    properties = backend.properties(datetime=time)

    for gate in properties.gates:
        for param in gate.parameters:
            if param.name == 'gate_error':
                depol_params[gate.name] = _gate_fidelity_to_lambda(1-param.value, 2**(len(gate.qubits)))

            elif param.name == 'gate_length':
                gate_times[gate.name] = param.value * 1e-9

    for qubit in properties.qubits:
        for param in qubit:
            if param.name == 'T1':
                t1_times.append(param.value * 1e-6)
            elif param.name == 'T2':
                t2_times.append(param.value * 1e-6)

    return depol_params, gate_times, t1_times, t2_times

def _gate_fidelity_to_lambda(f, d):
    return (d*f - d)/(1-d)