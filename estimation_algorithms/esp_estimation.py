def esp(circ, backend, time=None):
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