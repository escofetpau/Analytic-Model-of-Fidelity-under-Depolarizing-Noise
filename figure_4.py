import csv
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

def scatter_hist(y, ax_histy, color):
    # no labels
    ax_histy.tick_params(axis="y", labelleft=False)
    ax_histy.tick_params(axis="x", labelbottom=False)
    ax_histy.xaxis.set_visible(False)

    ax_histy.hist(y, bins=10, orientation='horizontal', density=True, alpha=0.5, color=color)
    kde = stats.gaussian_kde(y)
    x = np.linspace(-1, 1, 1000)
    ax_histy.plot(kde(x), x, color=color, linewidth=2)

scatter_size = 50
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

qiskit_diff = [fid_qiskit[i] - sr_mit_IBMQ[i] for i in range(len(fid_qiskit))]
esp_diff = [fid_esp[i] - sr_mit_IBMQ[i] for i in range(len(fid_esp))]
qva_diff = [fid_avg_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_qva))]
qva_0_diff = [fid_max_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_max_qva))]
depol_diff = [fid_avg_depol[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol))]
depol_thermal_diff = [fid_avg_depol_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol_thermal))]

y_lims = (-0.5, 1)

fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(19, 7), sharey=True, sharex=True)

# Qiskit
axs[0][0].scatter(num_gates, qiskit_diff, c='tab:blue', alpha=0.75, s=scatter_size)
axs[0][0].set_title('Qiskit', fontsize=label_size*1.2)

ax_histy = axs[0][0].inset_axes([1.05, 0, 0.25, 1], sharey=axs[0][0])
scatter_hist(qiskit_diff, ax_histy, 'tab:blue')
ax_histy.set_ylim(y_lims[0], y_lims[1])

# ESP
axs[0][1].scatter(num_gates, esp_diff, c='tab:orange', alpha=0.75, s=scatter_size)
axs[0][1].set_title('ESP', fontsize=label_size*1.2)

ax_histy = axs[0][1].inset_axes([1.05, 0, 0.25, 1], sharey=axs[0][1])
scatter_hist(esp_diff, ax_histy, 'tab:orange')
ax_histy.set_ylim(y_lims[0], y_lims[1])

# QVA
axs[0][2].scatter(num_gates, qva_diff, c='tab:red', alpha=0.75, s=scatter_size)
axs[0][2].set_title('QVA', fontsize=label_size*1.2)

ax_histy = axs[0][2].inset_axes([1.05, 0, 0.25, 1], sharey=axs[0][2])
scatter_hist(qva_diff, ax_histy, 'tab:red')
ax_histy.set_ylim(y_lims[0], y_lims[1])

# QVA 0
axs[1][0].scatter(num_gates, qva_0_diff, c='tab:red', alpha=0.75, s=scatter_size, marker='x')
axs[1][0].set_title('QVA $w=0$', fontsize=label_size*1.2)
axs[1][0].set_xlabel('Num. of Gates', fontsize=label_size)

ax_histy = axs[1][0].inset_axes([1.05, 0, 0.25, 1], sharey=axs[1][0])
scatter_hist(qva_0_diff, ax_histy, 'tab:red')
ax_histy.set_ylim(y_lims[0], y_lims[1])

# Depol
axs[1][1].scatter(num_gates, depol_diff, c='tab:green', alpha=0.75, s=scatter_size)
axs[1][1].set_title('This Work', fontsize=label_size*1.2)
axs[1][1].set_xlabel('Num. of Gates', fontsize=label_size)

ax_histy = axs[1][1].inset_axes([1.05, 0, 0.25, 1], sharey=axs[1][1])
scatter_hist(depol_diff, ax_histy, 'tab:green')
ax_histy.set_ylim(y_lims[0], y_lims[1])

# Depol Thermal
axs[1][2].scatter(num_gates, depol_thermal_diff, c='tab:green', alpha=0.75, s=scatter_size, marker='x')
axs[1][2].set_title('This Work + $T_{1,2}$', fontsize=label_size*1.2)
axs[1][2].set_xlabel('Num. of Gates', fontsize=label_size)

ax_histy = axs[1][2].inset_axes([1.05, 0, 0.25, 1], sharey=axs[1][2])
scatter_hist(depol_thermal_diff, ax_histy, 'tab:green')
ax_histy.set_ylim(y_lims[0], y_lims[1])

axs[0][0].set_ylabel('Fidelity\nDifference', fontsize=label_size)
axs[1][0].set_ylabel('Fidelity\nDifference', fontsize=label_size)
for row in axs:
    for ax in row:
        ax.set_box_aspect(0.7)
        ax.set_xscale('log')

        ax.axhline(0, color='tab:gray', linestyle='--', zorder=-10)
        ax.tick_params(axis='both', which='major', labelsize=ticks_size)
        ax.set_yticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])

# set subplots spacing parameters
plt.subplots_adjust(left=0.015, bottom=0.1, right=1, top=0.94, wspace=0, hspace=0.2)

plt.show()