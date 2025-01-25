import numpy as np

def qva(circ, backend, w=0, time=None):
    error_params, _, _, _ = _backend_to_errors(backend, time=time)

    CSR = [1.0 for _ in backend.properties().qubits]
    for gate in circ:
        if gate.operation.num_qubits == 1:
            if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}' in error_params:
                qubit = circ.find_bit(gate.qubits[0]).index
                CSR[qubit] *= error_params[f'{gate.operation.name}{qubit}']
        
        else:
            if f'{gate.operation.name}{circ.find_bit(gate.qubits[0]).index}_{circ.find_bit(gate.qubits[1]).index}' in error_params:
                qubit_1 = circ.find_bit(gate.qubits[0]).index
                qubit_2 = circ.find_bit(gate.qubits[1]).index

                fid_1 = CSR[qubit_1]
                fid_2 = CSR[qubit_2]

                crosserror_1 = (1 - fid_2) * w
                crosserror_2 = (1 - fid_1) * w

                CSR[qubit_1] = fid_1 * error_params[f'{gate.operation.name}{qubit_1}_{qubit_2}'] * (1-crosserror_1)
                CSR[qubit_2] = fid_2 * error_params[f'{gate.operation.name}{qubit_1}_{qubit_2}'] * (1-crosserror_2)
    
    return(np.prod(CSR))


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