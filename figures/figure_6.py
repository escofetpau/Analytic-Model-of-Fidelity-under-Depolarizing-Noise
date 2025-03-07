import matplotlib.pyplot as plt
import csv
import numpy as np

scatter_size = 50
ticks_size = 15
label_size = 20
plot_width = 2.5

file = open(f'../data/shor_computation_data.csv', 'r')
data = list(csv.reader(file, delimiter=","))
file.close()

p1s = [float(i) for i in data[0]]
p2s = [float(i) for i in data[1]]

fidelities = []

for i in range(len(p1s)):
    fidelities.append([float(j) for j in data[i+2]])

thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]

thresh_plots = [[] for _ in thresholds]
for i,th in enumerate(thresholds):
    for j in range(len(p1s)):
        rightmost_point = 0
        for k in range(len(p2s)):
            if fidelities[j][k] > th:
                rightmost_point = p2s[k]
        thresh_plots[i].append(rightmost_point)

fig, ax = plt.subplots(figsize=(12, 6), layout='compressed')
X,Y = np.meshgrid(p2s, p1s)

color = ax.pcolormesh(X, Y, fidelities, cmap='inferno')
cbar = fig.colorbar(color, pad=0.02)
cbar.set_label('Fidelity', fontsize=label_size)
cbar.ax.tick_params(labelsize=ticks_size)

for i,th in enumerate(thresholds):
    ax.plot([thresh_plots[i][0], thresh_plots[i][-1]], [p1s[0], p1s[-1]], linewidth=plot_width, color='snow')
    ax.text(thresh_plots[i][-1], p1s[-1], f' {th}', fontsize=ticks_size, color='snow', va='top', ha='left', fontweight='bold')

ax.set_ylabel('Single-qubit gate depolarization\n$p_1$', fontsize=label_size)
ax.set_xlabel('Two-qubit gate depolarization\n$p_2$', fontsize=label_size)

ax.ticklabel_format(axis='both', style='sci', scilimits=(0,0))

# set ticks to scientific notation
ax.xaxis.set_tick_params(labelsize=ticks_size)
ax.yaxis.set_tick_params(labelsize=ticks_size)

plt.show()