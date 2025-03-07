import csv
import matplotlib.pyplot as plt

scatter_size = 20
ticks_size = 15
label_size = 20
fig, ax = plt.subplots(figsize=(20, 7))

file = open('../data/data_1.csv', 'r')
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

ax.scatter(num_gates, fid_qiskit, label='Qiskit', color='tab:blue', alpha=0.75, s=[scatter_size*q for q in num_qubits])
ax.scatter(num_gates, fid_esp, label='ESP', color='tab:orange', alpha=0.75, s=[scatter_size*q for q in num_qubits])
ax.scatter(num_gates, fid_avg_qva, label='QVA', color='tab:red', alpha=0.75, s=[scatter_size*q for q in num_qubits])

ax.scatter(num_gates, sr_mit_IBMQ, label='IBMQ mit', color='tab:purple', alpha=0.75, s=[scatter_size*q for q in num_qubits])


# error bars
ax.errorbar(num_gates, fid_avg_qva, yerr=qva_error, fmt='o', c='gray', markersize=0, alpha=0.5, zorder=-1)


ax.set_xscale('log')
ax.set_xlabel('Number of Gates', fontsize=label_size)
ax.set_ylabel('Fidelity', fontsize=label_size)

ax.tick_params(axis='both', which='major', labelsize=ticks_size)

# add new axis
## Add zoom in axes
y_bottom = 0.1
y_top = ax.get_ylim()[1] * 0.65
axins = ax.inset_axes([13, y_bottom, 45, y_top-y_bottom], transform=ax.transData)
axins.set_facecolor('snow')

qiskit_diff = [fid_qiskit[i] - sr_mit_IBMQ[i] for i in range(len(fid_qiskit))]
esp_diff = [fid_esp[i] - sr_mit_IBMQ[i] for i in range(len(fid_esp))]
qva_diff = [fid_avg_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_qva))]
qva_min_diff = [fid_min_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_min_qva))]
qva_max_diff = [fid_max_qva[i] - sr_mit_IBMQ[i] for i in range(len(fid_max_qva))]
depol_diff = [fid_avg_depol[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol))]
depol_thermal_diff = [fid_avg_depol_thermal[i] - sr_mit_IBMQ[i] for i in range(len(fid_avg_depol_thermal))]

colors = ['tab:blue', 'tab:orange', 'tab:red', 'tab:red', 'tab:red']
box = axins.boxplot([qiskit_diff, esp_diff, qva_min_diff, qva_diff, qva_max_diff], positions=[1, 2, 3, 3.5, 4], labels=['Qiskit', 'ESP', 'QVA\nmin', 'QVA', 'QVA\nmax'], patch_artist=True, widths=0.45)

for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
    patch.set_edgecolor('black')
    for median in box['medians']:
        median.set_color('black')



############## PLOT DEPOL RESULTS ################
# ax.scatter(num_gates, fid_avg_depol, label='This Work', color='tab:green', alpha=0.75, s=[scatter_size*q for q in num_qubits])
# ax.scatter(num_gates, fid_avg_depol_thermal, label='This Work +$T_{1,2}$', color='tab:green', alpha=0.75, marker = 'x', s=[scatter_size*q for q in num_qubits])
# box = axins.boxplot([depol_diff, depol_thermal_diff], positions=[5, 5.5], labels=['This Work', 'This Work\n+$T_{1,2}$'], patch_artist=True, widths=0.45)
# for patch in box['boxes']:
#     patch.set_facecolor('tab:green')
#     patch.set_alpha(0.75)
#     patch.set_edgecolor('black')
#     for median in box['medians']:
#         median.set_color('black')
##################################################


ax.legend(fontsize=ticks_size, ncols=1)


# ticks size
axins.tick_params(axis='both', which='major', labelsize=ticks_size*0.85)
axins.tick_params(axis='x', which='major', labelsize=ticks_size*0.85, rotation=45)
axins.set_ylabel('Fidelity Difference', fontsize=label_size*0.85, labelpad=-3)
axins.axhline(y=0, color='gray', linestyle='--', zorder=-10)

plt.tight_layout()
plt.show()