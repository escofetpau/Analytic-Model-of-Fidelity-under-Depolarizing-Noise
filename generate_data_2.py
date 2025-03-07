from qiskit_ibm_runtime import QiskitRuntimeService

from estimation_algorithms.depolarizing_estimation import depolarizing
from estimation_algorithms.esp_estimation import esp
from estimation_algorithms.qva_estimation import qva
from estimation_algorithms.qiskit_estimation import qiskit_fidelity, qiskit_counts
from estimation_algorithms.mitigate_counts import mitigate

import pickle
import csv
from datetime import datetime

def sr_from_counts(counts_1, counts_2):
    sr = 0
    for key in counts_1:
        if key in counts_2:
            sr += min(counts_1[key], counts_2[key])
    return sr/2048


experiment = 'ADD EXPERIMENT NAME HERE (print from generate_data_1.py)'

circuits = pickle.load(open(experiment + '_circuits', 'rb'))
file = open(experiment + '.csv', 'r')
data = list(csv.reader(file, delimiter=","))
file.close()

token = data[0][0]
executed_filenames = data[1]
num_qubits = data[2]
num_qubits = [int(q) for q in num_qubits]
job_id = data[3][0]
backend_name = data[4][0]

service = QiskitRuntimeService(channel="ibm_quantum", token=token)
job = service.job(job_id)
raw_counts = [res.data.meas.get_counts() if 'meas' in res.data else res.data.c.get_counts() for res in job.result()]

backend = job.backend()
running_time = datetime.fromisoformat(job.metrics()['timestamps']['running'])

depths = []
gates = []

fid_qiskit = []
fid_qiskit_thermal = []
fid_esp = []
fid_esp_thermal = []
fid_qva = []
fid_qva_thermal = []
fid_depol = []
fid_depol_thermal = []

sr_raw_IBMQ = []
sr_mit_IBMQ = []

qiskit_noise_model = noise.NoiseModel.from_backend(backend, thermal_relaxation=True)
depol_error_params, gate_times, t1_times, t2_times = depol_backend_errors(backend, time=running_time)
esp_qva_error_params, _, _, _ = esp_qva_backend_errors(backend, time=running_time)

for i,circ in enumerate(circuits):
    print(f'{i} out of {len(circuits)} with gates {len(circ.data)}')

    depths.append(circ.depth())
    gates.append(len(circ.data))

    sr_raw_IBMQ.append(raw_counts[i]['0'*len(list(raw_counts[i].keys())[0])]/2048)

    mit_counts = mitigate(circ, raw_counts[i], backend, time=running_time)
    sr_mit_IBMQ.append(mit_counts['0'*len(list(mit_counts.keys())[0])]/2048)

    fid_qiskit.append(qiskit_fidelity(circ, backend, time=running_time, noise_model=qiskit_noise_model))
    fid_qiskit_thermal.append(qiskit_fidelity_thermal(circ, backend, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times, noise_model=qiskit_noise_model))
    fid_esp.append(esp(circ, backend, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times))
    fid_esp_thermal.append(esp_thermal(circ, backend, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times))
    fid_qva.append((qva(circ, backend, w=1, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times), qva(circ, backend, w=0, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times)))
    fid_qva_thermal.append((qva_thermal(circ, backend, w=1, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times), qva_thermal(circ, backend, w=0, time=running_time, error_params=esp_qva_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times)))
    fid_depol.append((depolarizing(circ, backend, p=1, time=running_time, error_params=depol_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times), depolarizing(circ, backend, p=0, time=running_time, error_params=depol_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times)))
    fid_depol_thermal.append((depolarizing_thermal(circ, backend, p=1, time=running_time, error_params=depol_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times), depolarizing_thermal(circ, backend, p=0, time=running_time, error_params=depol_error_params, gate_times=gate_times, t1_times=t1_times, t2_times=t2_times)))

with open(experiment + '_results.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(executed_filenames)
    writer.writerow(num_qubits)
    writer.writerow(depths)
    writer.writerow(gates)

    writer.writerow(fid_qiskit)
    writer.writerow(fid_qiskit_thermal)
    writer.writerow(fid_esp)
    writer.writerow(fid_esp_thermal)
    writer.writerow(fid_qva)
    writer.writerow(fid_qva_thermal)
    writer.writerow(fid_depol)
    writer.writerow(fid_depol_thermal)

    writer.writerow(sr_raw_IBMQ)
    writer.writerow(sr_mit_IBMQ)