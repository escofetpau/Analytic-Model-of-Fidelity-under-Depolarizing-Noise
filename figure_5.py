from matplotlib import pyplot as plt
import csv
import numpy as np


scatter_size = 50
ticks_size = 15
label_size = 20
plot_width = 2.5

styles = ['-', '--', '-.', ':']


file = open(f'link_feasibility_data.csv', 'r')
data = list(csv.reader(file, delimiter=","))
file.close()

sizes = [int(i) for i in data[0]]
p1 = [float(i) for i in data[1]]
p1_label = ['$p_1=0$', '$p_1=10^{-7}$', '$p_1=10^{-6}$']

qft_l = [[float(i) for i in row] for row in data[2:2+len(p1)]]
qvol_l = [[float(i) for i in row] for row in data[2+len(p1):2+2*len(p1)]]
cdkm_l = [[float(i) for i in row] for row in data[2+2*len(p1):2+3*len(p1)]]
draper_l = [[float(i) for i in row] for row in data[2+3*len(p1):2+4*len(p1)]]
ghz_l = [[float(i) for i in row] for row in data[2+4*len(p1):2+5*len(p1)]]

fig, ax = plt.subplots(ncols=1, figsize=(10, 5))

for i in range(len(p1)):
    # for each circuit plot only values different than -1
    valid_elem = len([j for j in range(len(qft_l[i])) if qft_l[i][j] != -1])
    ax.plot(sizes[:valid_elem], qft_l[i][:valid_elem], color='tab:blue', linewidth=plot_width, linestyle=styles[i], alpha=0.75)

    valid_elem = len([j for j in range(len(qvol_l[i])) if qvol_l[i][j] != -1])
    ax.plot(sizes[:valid_elem], qvol_l[i][:valid_elem], color='tab:green', linewidth=plot_width, linestyle=styles[i], alpha=0.75)
    
    valid_elem = len([j for j in range(len(cdkm_l[i])) if cdkm_l[i][j] != -1])
    ax.plot(sizes[:valid_elem], cdkm_l[i][:valid_elem], color='tab:red', linewidth=plot_width, linestyle=styles[i], alpha=0.75)

    valid_elem = len([j for j in range(len(draper_l[i])) if draper_l[i][j] != -1])
    ax.plot(sizes[:valid_elem], draper_l[i][:valid_elem], color='tab:purple', linewidth=plot_width, linestyle=styles[i], alpha=0.75)

    valid_elem = len([j for j in range(len(ghz_l[i])) if ghz_l[i][j] != -1])
    ax.plot(sizes[:valid_elem], ghz_l[i][:valid_elem], color='tab:orange', linewidth=plot_width, linestyle=styles[i], alpha=0.75)

ax.set_xlabel('Number of qubits', fontsize=label_size)
ax.set_ylabel('2-qubit gate $p_2$', fontsize=label_size)

ax.plot([], [], color='tab:blue', linewidth=plot_width, label='QFT')
ax.plot([], [], color='tab:green', linewidth=plot_width, label='QVolume')
ax.plot([], [], color='tab:red', linewidth=plot_width, label='Cuccaro Adder')
ax.plot([], [], color='tab:purple', linewidth=plot_width, label='Draper Adder')
ax.plot([], [], color='tab:orange', linewidth=plot_width, label='GHZ')

ax.plot([], [], color='tab:orange', linewidth=0, label=' ')

ax.axhline(y=p1[1], color='gray', linestyle=styles[1], linewidth=1.5, alpha=0.75, zorder=-1)
ax.axhline(y=p1[2], color='gray', linestyle=styles[2], linewidth=1.5, alpha=0.75, zorder=-1)

ax.text(x=11, y=p1[1], s=p1_label[1], fontsize=ticks_size, color='gray', ha='left', va='bottom')
ax.text(x=11, y=p1[2], s=p1_label[2], fontsize=ticks_size, color='gray', ha='left', va='bottom')

for i in range(len(p1)):
    ax.plot([], [], color='black', linewidth=plot_width, linestyle=styles[i], label=p1_label[i])

ax.set_xlim([min(sizes), max(sizes)])
ax.set_yscale('log')

ax.legend(fontsize=ticks_size*0.9, ncols=3)

# ticks size
ax.tick_params(axis='both', which='major', labelsize=ticks_size)

plt.tight_layout()
plt.show()