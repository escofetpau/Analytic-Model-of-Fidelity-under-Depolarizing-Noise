from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import qiskit

from os import listdir
from os.path import join
import csv
from datetime import datetime
import pickle

token = 'ADD YOUR IBMQ TOKEN HERE'

service = QiskitRuntimeService(channel="ibm_quantum", token=token)
backend = service.least_busy(simulator=False, operational=True)
backend_name = backend.name
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

bench_path = 'circuits'

filenames = sorted([f for f in listdir(bench_path)])
executed_filenames = []

circuits_to_execute = []
num_qubits = []

for f, file in enumerate(filenames):
    print(f'{file}', f'{f} out of {len(filenames)}')

    circ = qiskit.circuit.QuantumCircuit.from_qasm_file(join(bench_path, file))

    circ_inv = circ.copy()
    circ_inv.remove_final_measurements()
    circ_inv = circ_inv.inverse()
    circ_inv.barrier()

    rev_circ = circ_inv & circ

    isa_circ = pm.run(rev_circ)

    if isa_circ.depth() >= 5000:
        print('\tBenchmark not executed, depth =', isa_circ.depth())
        continue

    num_qubits.append(circ.num_qubits)
    executed_filenames.append(file)
    circuits_to_execute.append(isa_circ)

with Session(backend=backend):
    sampler = Sampler()
    job = sampler.run(circuits_to_execute, shots=2048)
    job_id = job.job_id()

    date = datetime.now().isoformat()

    pickle.dump(circuits_to_execute, open(f'IBMQ_{date}_circuits', 'wb'))

    # Save results into csv file
    with open(f'IBMQ_{date}.csv', mode='w') as file:
        writer = csv.writer(file)

        writer.writerow([token])
        writer.writerow(executed_filenames)
        writer.writerow(num_qubits)
        writer.writerow([job_id])
        writer.writerow([backend_name])

    print(f'rev_IBMQ_{date}')