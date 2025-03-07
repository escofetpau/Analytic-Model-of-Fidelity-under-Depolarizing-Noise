import csv
import matplotlib.pyplot as plt
from os.path import join
from sklearn.metrics import r2_score
import numpy as np
from sklearn.metrics import r2_score
from scipy import stats

scatter_size = 50
ticks_size = 15
label_size = 20

def scatter_hist(y, ax_histy, color):
    # no labels
    ax_histy.tick_params(axis="y", labelleft=False)
    ax_histy.tick_params(axis="x", labelbottom=False)
    ax_histy.xaxis.set_visible(False)

    ax_histy.hist(y, bins=10, orientation='horizontal', density=True, alpha=0.5, color=color)
    kde = stats.gaussian_kde(y)
    x = np.linspace(-1, 1, 1000)
    ax_histy.plot(kde(x), x, color=color, linewidth=2)

experiments = [
    'data_1',
    'data_2',
    'data_3',
    'data_4',
    'data_5',
    'data_6'
]

fig, axs = plt.subplots(5, len(experiments), figsize=(9, 15), sharey=True)

for i, experiment in enumerate(experiments):
    file = open(experiment +'.csv', 'r')

    data = list(csv.reader(file, delimiter=","))

    filenames = data[0]
    num_qubits = [int(q) for q in data[1]]
    depths = [int(d) for d in data[2]]
    num_gates = [int(g) for g in data[3]]

    fid_qiskit = [float(f) for f in data[4]]
    fid_qiskit_thermal = [float(f) for f in data[5]]

    fid_esp = [float(f) for f in data[6]]
    fid_esp_thermal = [float(f) for f in data[7]]

    fid_min_qva = [float(eval(f)[0]) for f in data[8]]
    fid_max_qva = [float(eval(f)[1]) for f in data[8]]
    fid_avg_qva = [(fid_min_qva[i] + fid_max_qva[i])/2 for i in range(len(fid_min_qva))]
    qva_error = [(fid_max_qva[i]-fid_min_qva[i])/2 for i in range(len(fid_min_qva))]

    fid_min_qva_thermal = [float(eval(f)[0]) for f in data[9]]
    fid_max_qva_thermal = [float(eval(f)[1]) for f in data[9]]
    fid_avg_qva_thermal = [(fid_min_qva_thermal[i] + fid_max_qva_thermal[i])/2 for i in range(len(fid_min_qva_thermal))]
    qva_thermal_error = [(fid_max_qva_thermal[i]-fid_min_qva_thermal[i])/2 for i in range(len(fid_min_qva_thermal))]

    fid_min_depol = [float(eval(f)[0]) for f in data[10]]
    fid_max_depol = [float(eval(f)[1]) for f in data[10]]
    fid_avg_depol = [(fid_min_depol[i] + fid_max_depol[i])/2 for i in range(len(fid_min_depol))]
    depol_error = [(fid_max_depol[i]-fid_min_depol[i])/2 for i in range(len(fid_min_depol))]

    fid_min_depol_thermal = [float(eval(f)[0]) for f in data[11]]
    fid_max_depol_thermal = [float(eval(f)[1]) for f in data[11]]
    fid_avg_depol_thermal = [(fid_min_depol_thermal[i] + fid_max_depol_thermal[i])/2 for i in range(len(fid_min_depol_thermal))]
    depol_thermal_error = [(fid_max_depol_thermal[i]-fid_min_depol_thermal[i])/2 for i in range(len(fid_min_depol_thermal))]

    sr_raw_IBMQ = [float(f) for f in data[12]]
    sr_mit_IBMQ = [float(f) for f in data[13]]

    qiskit_diff = [fid_qiskit[i] - sr_mit_IBMQ[i] for i in range(len(fid_qiskit))]
    qiskit_thermal_diff = [fid_qiskit_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_qiskit_thermal))]
    esp_diff = [fid_esp[i] - sr_mit_IBMQ[i] for i in range(len(fid_esp))]
    esp_thermal_diff = [fid_esp_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_esp_thermal))]
    qva_diff = [fid_avg_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_qva))]
    qva_thermal_diff = [fid_avg_qva_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_qva_thermal))]
    qva_max_thermal_diff = [fid_max_qva_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_max_qva_thermal))]
    depol_diff = [fid_avg_depol[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol))]
    depol_thermal_diff = [fid_avg_depol_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol_thermal))]

    scatter_hist(qiskit_thermal_diff, axs[0, i], 'tab:blue')
    scatter_hist(esp_thermal_diff, axs[1, i], 'tab:orange')
    scatter_hist(qva_thermal_diff, axs[2, i], 'tab:red')
    scatter_hist(qva_max_thermal_diff, axs[3, i], 'tab:red')
    scatter_hist(depol_thermal_diff, axs[4, i], 'tab:green')

    # Add R2 score to each plot
    r2_qiskit = r2_score(sr_mit_IBMQ, fid_qiskit_thermal)
    r2_esp = r2_score(sr_mit_IBMQ, fid_esp_thermal)
    r2_qva = r2_score(sr_mit_IBMQ, fid_avg_qva_thermal)
    r2_qva_max = r2_score(sr_mit_IBMQ, fid_max_qva_thermal)
    r2_depol = r2_score(sr_mit_IBMQ, fid_avg_depol_thermal)

    axs[0, i].text(axs[0, i].get_xlim()[1], -1, f'R2: {np.round(r2_qiskit, 2)}', horizontalalignment='right', verticalalignment='center', fontsize=15)
    axs[1, i].text(axs[1, i].get_xlim()[1], -1, f'R2: {np.round(r2_esp, 2)}', horizontalalignment='right', verticalalignment='center', fontsize=15)
    axs[2, i].text(axs[2, i].get_xlim()[1], -1, f'R2: {np.round(r2_qva, 2)}', horizontalalignment='right', verticalalignment='center', fontsize=15)
    axs[3, i].text(axs[3, i].get_xlim()[1], -1, f'R2: {np.round(r2_qva_max, 2)}', horizontalalignment='right', verticalalignment='center', fontsize=15)
    axs[4, i].text(axs[4, i].get_xlim()[1], -1, f'R2: {np.round(r2_depol, 2)}', horizontalalignment='right', verticalalignment='center', fontsize=15)


axs[0, 0].set_ylabel('Qiskit\n+ $T_{1,2}$', fontsize=label_size)
axs[1, 0].set_ylabel('ESP\n+ $T_{1,2}$', fontsize=label_size)
axs[2, 0].set_ylabel('QVA\n+ $T_{1,2}$', fontsize=label_size)
axs[3, 0].set_ylabel('QVA$_{w=0}$\n+ $T_{1,2}$', fontsize=label_size)
axs[4, 0].set_ylabel('This Work\n+ $T_{1,2}$', fontsize=label_size)

for i in range(5):
    axs[i, 0].tick_params(axis="y", labelleft=True)
    axs[i, 0].set_yticks([-1, -0.5, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1], fontsize=ticks_size)

for i in range(len(experiments)):
    axs[0, i].set_title(f'Exec. {i+1}', fontsize=label_size, rotation=45)

# set plot params margins
plt.subplots_adjust(left=0.14, right=0.99, top=0.91, bottom=0.01, hspace=0.11)
plt.show()