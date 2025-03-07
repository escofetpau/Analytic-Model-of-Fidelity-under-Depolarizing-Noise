import csv
import matplotlib.pyplot as plt
from os.path import join
from sklearn.metrics import r2_score
import numpy as np
from scipy import stats

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

file = open('../data/data_depol_simulation.csv', 'r')
data = list(csv.reader(file, delimiter=","))

filenames = data[0]
num_qubits = [int(q) for q in data[1]]
depths = [int(d) for d in data[2]]
num_gates = [int(g) for g in data[3]]

fid_qiskit = [float(f) for f in data[4]]
fid_min_depol = [float(eval(f)[0]) for f in data[5]]
fid_max_depol = [float(eval(f)[1]) for f in data[5]]
fid_avg_depol = [(fid_min_depol[i] + fid_max_depol[i])/2 for i in range(len(fid_min_depol))]
depol_error = [(fid_max_depol[i]-fid_min_depol[i])/2 for i in range(len(fid_min_depol))]

depol_diff = [fid_avg_depol[i] - fid_qiskit[i] for i in range(len(fid_avg_depol))]

y_lims = (-1, 1)

fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(14, 4))

# Depol vs Simulation
axs[0].scatter(fid_avg_depol, fid_qiskit, c='tab:green', alpha=0.75, s=scatter_size)
axs[0].errorbar(fid_avg_depol, fid_qiskit, xerr=depol_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)
axs[0].plot([0,1], [0,1], color='tab:gray')
axs[0].set_ylabel('Simulated Fidelity', fontsize=label_size)
axs[0].set_xlabel('This Work Pred. Fidelity', fontsize=label_size)

# Depol Difference
axs[1].scatter(num_gates, depol_diff, c='tab:green', alpha=0.75, s=scatter_size)
axs[1].errorbar(num_gates, depol_diff, yerr=depol_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)
axs[1].set_xlabel('Num. of Gates', fontsize=label_size)

ax_histy = axs[1].inset_axes([1.05, 0, 0.25, 1], sharey=axs[1])
scatter_hist(depol_diff, ax_histy, 'tab:green')
ax_histy.set_ylim(y_lims[0], y_lims[1])

axs[0].set_box_aspect(1)
axs[0].set_xlim(0, 1)
axs[0].set_ylim(0, 1)
axs[0].tick_params(axis='both', which='major', labelsize=ticks_size)
axs[0].set_xticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.5', '0.75', '1'])
axs[0].set_yticks([0, 0.25, 0.5, 0.75, 1], ['0', '0.25', '0.5', '0.75', '1'])

axs[1].set_box_aspect(0.6)
axs[1].set_xscale('log')
axs[1].axhline(0, color='tab:gray', linestyle='--', zorder=-10)
axs[1].tick_params(axis='both', which='major', labelsize=ticks_size)
axs[1].set_ylabel('Fidelity\nDifference', fontsize=label_size)

plt.subplots_adjust(left=0, bottom=0.17, right=0.88, top=0.95, wspace=0, hspace=0.2)

plt.show()