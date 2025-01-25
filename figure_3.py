import csv
import matplotlib.pyplot as plt

scatter_size = 60
ticks_size = 15
label_size = 20

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


fig, axs = plt.subplots(ncols=5, nrows=1, figsize=(20, 4.5), sharey=True)

# Qiskit
axs[0].scatter(fid_qiskit, sr_mit_IBMQ, c='tab:blue', alpha=0.75, s=scatter_size)
axs[0].plot([0,1], [0,1], color='tab:gray')
axs[0].set_title('Qiskit', fontsize=label_size*1.2)
axs[0].set_ylabel('Circuit Success Rate', fontsize=label_size)

# ESP
axs[1].scatter(fid_esp, sr_mit_IBMQ, c='tab:orange', alpha=0.75, s=scatter_size)
axs[1].plot([0,1], [0,1], color='tab:gray')
axs[1].set_title('ESP', fontsize=label_size*1.2)

# QVA
axs[2].scatter(fid_avg_qva, sr_mit_IBMQ, c='tab:red', alpha=0.75, s=scatter_size)
axs[2].errorbar(fid_avg_qva, sr_mit_IBMQ, xerr=qva_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)
axs[2].plot([0,1], [0,1], color='tab:gray')
axs[2].set_title('QVA', fontsize=label_size*1.2)

# Depol
axs[3].scatter(fid_avg_depol, sr_mit_IBMQ, c='tab:green', alpha=0.75, s=scatter_size)
axs[3].errorbar(fid_avg_depol, sr_mit_IBMQ, xerr=depol_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)
axs[3].plot([0,1], [0,1], color='tab:gray')
axs[3].set_title('This Work', fontsize=label_size*1.2)

# Depol Thermal
axs[4].scatter(fid_avg_depol_thermal, sr_mit_IBMQ, c='tab:green', marker='x', alpha=0.75, s=scatter_size)
axs[4].errorbar(fid_avg_depol_thermal, sr_mit_IBMQ, xerr=depol_thermal_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)
axs[4].plot([0,1], [0,1], color='tab:gray')
axs[4].set_title('This Work + $T_{1,2}$', fontsize=label_size*1.2)

axs[0].set_yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.5', '0.75', '1'])
for ax in axs:
    ax.set_box_aspect(1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.set_xlabel('Pred. Fidelity', fontsize=label_size)

    ax.tick_params(axis='both', which='major', labelsize=ticks_size)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.5', '0.75', '1'])

plt.tight_layout()
plt.show()