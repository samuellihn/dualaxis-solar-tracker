import csv

import numpy as np
from matplotlib import pyplot as plt

src_dir = "data/processed/"
src_files = [
    ["Static Panel", "Trial 2/static_96s.csv"],
    ["Tracking Panel, 500ms Adjustment Time", "Trial 2/tracker_500ms_96s.csv"],
    ["Tracking Panel, 1000ms Adjustment Time", "Trial 2/tracker_1000ms_96s.csv"],
    ["Tracking Panel, 2000ms Adjustment Time", "Trial 2/tracker_2000ms_96s.csv"],
    ["Tracking Panel, 3000ms Adjustment Time", "Trial 2/tracker_3000ms_96s.csv"],
    ["Tracking Panel, 4000ms Adjustment Time", "Trial 2/tracker_4000ms_96s.csv"],
    ["Tracking Panel, 6000ms Adjustment Time", "Trial 2/tracker_6000ms_96s.csv"],
    ["Tracking Panel, 8000ms Adjustment Time", "Trial 2/tracker_8000ms_96s.csv"],
]

dest_graph_dir = "graphs/"

intervals = [0, 500, 1000, 2000, 3000, 4000, 6000, 8000]
labels = ["Static"] + [f"{i}ms" for i in intervals[1:]]


def csv_to_ndarray(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)

        data = []
        for row in csv_reader:
            data.append(row)
        return np.array(data, dtype=np.float)


fig, ax = plt.subplots(figsize=(12, 8))
energies = []
for file in src_files:
    data_array = csv_to_ndarray(src_dir + file[1])

    milliwatts = [i[0] * i[1] for i in zip(data_array[:, 1], data_array[:, 1])]
    millijoules = np.trapz(milliwatts, data_array[:, 0])
    energies.append(millijoules)
for i in range(len(intervals)):
    ax.annotate(labels[i], (intervals[i]+100, energies[i]-1))

ax.scatter(intervals, energies, c=np.random.rand(len(intervals), 3))
ax.set_title("Adjustment Interval vs. Total Energy Generated")
ax.set_xlabel('Adjustment Interval (milliseconds)')  # Add an x-label to the axes.
ax.set_xbound(0, 9000)
ax.set_ylabel('Energy (millijoules)')  # Add a y-label to the axes.
ax.set_xticks(np.arange(0, 8001, 500))  # setting the ticks

plt.savefig(dest_graph_dir + "Adjustment Frequency vs. Energy" + ".png")

plt.show()
