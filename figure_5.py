import csv
import matplotlib.pyplot as plt
import numpy as np

scatter_size = 50
ticks_size = 15
label_size = 20
plot_width = 3

file = open('data.csv', 'r')
data = list(csv.reader(file, delimiter=","))

filenames = data[0]
num_qubits = [int(q) for q in data[1]]
depths = [int(d) for d in data[2]]
num_gates = [int(g) for g in data[3]]

fid_qiskit = [float(f) for f in data[4]]
fid_esp = [float(f) for f in data[5]]
fid_min_qva = [float(eval(f)[0]) for f in data[6]]
fid_max_qva = [float(eval(f)[1]) for f in data[6]]
fid_avg_qva = [(fid_min_qva[i] + fid_max_qva[i])/2 for i in range(len(fid_min_qva))]
qva_error = [(fid_max_qva[i]-fid_min_qva[i])/2 for i in range(len(fid_min_qva))]
fid_min_depol = [float(eval(f)[0]) for f in data[7]]
fid_max_depol = [float(eval(f)[1]) for f in data[7]]
fid_avg_depol = [(fid_min_depol[i] + fid_max_depol[i])/2 for i in range(len(fid_min_depol))]
depol_error = [(fid_max_depol[i]-fid_min_depol[i])/2 for i in range(len(fid_min_depol))]
fid_min_depol_thermal = [float(eval(f)[0]) for f in data[8]]
fid_max_depol_thermal = [float(eval(f)[1]) for f in data[8]]
fid_avg_depol_thermal = [(fid_min_depol_thermal[i] + fid_max_depol_thermal[i])/2 for i in range(len(fid_min_depol_thermal))]
depol_thermal_error = [(fid_max_depol_thermal[i]-fid_min_depol_thermal[i])/2 for i in range(len(fid_min_depol_thermal))]

sr_raw_IBMQ = [float(f) for f in data[9]]
sr_mit_IBMQ = [float(f) for f in data[10]]

qiskit_diff = [fid_qiskit[i] - sr_mit_IBMQ[i] for i in range(len(fid_qiskit))]
esp_diff = [fid_esp[i] - sr_mit_IBMQ[i] for i in range(len(fid_esp))]
qva_diff = [fid_avg_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_qva))]
qva_0_diff = [fid_max_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_max_qva))]
depol_diff = [fid_avg_depol[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol))]
depol_thermal_diff = [fid_avg_depol_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol_thermal))]

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12, 5))

threshold = np.linspace(0, 0.25, 100)

qiskit_accuracy = [len([i for i in range(len(num_gates)) if abs(qiskit_diff[i]) < t])/len(num_gates) for t in threshold]
esp_accuracy = [len([i for i in range(len(num_gates)) if abs(esp_diff[i]) < t])/len(num_gates) for t in threshold]
qva_accuracy = [len([i for i in range(len(num_gates)) if abs(qva_diff[i]) < t])/len(num_gates) for t in threshold]
qva_0_accuracy = [len([i for i in range(len(num_gates)) if abs(qva_0_diff[i]) < t])/len(num_gates) for t in threshold]
depol_accuracy = [len([i for i in range(len(num_gates)) if abs(depol_diff[i]) < t])/len(num_gates) for t in threshold]
depol_thermal_accuracy = [len([i for i in range(len(num_gates)) if abs(depol_thermal_diff[i]) < t])/len(num_gates) for t in threshold]

ax.plot(threshold, qiskit_accuracy, label='Qiskit', color='tab:blue', alpha=0.75, linewidth=plot_width)
ax.plot(threshold, esp_accuracy, label='ESP', color='tab:orange', alpha=0.75, linewidth=plot_width)
ax.plot(threshold, qva_accuracy, label='QVA', color='tab:red', alpha=0.75, linewidth=plot_width)
ax.plot(threshold, qva_0_accuracy, label='QVA 0', color='tab:red', alpha=0.75, linewidth=plot_width, linestyle='--')
ax.plot(threshold, depol_accuracy, label='Depol', color='tab:green', alpha=0.75, linewidth=plot_width)
ax.plot(threshold, depol_thermal_accuracy, label='Depol Thermal', color='tab:green', alpha=0.75, linewidth=plot_width, linestyle='--')


ax.tick_params(axis='both', which='major', labelsize=ticks_size)

ax.set_ylim(0, 1)

ax.set_xlabel('Threshold', fontsize=label_size)
ax.set_ylabel('Accuracy', fontsize=label_size)
ax.legend(fontsize=ticks_size)

plt.tight_layout()
plt.show()