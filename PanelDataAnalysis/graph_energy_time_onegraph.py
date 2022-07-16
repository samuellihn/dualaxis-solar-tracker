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
dest_graph_dir = "graphs/Energy vs. Time/"


def csv_to_ndarray(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)

        data = []
        for row in csv_reader:
            data.append(row)
        return np.array(data, dtype=np.float)


fig, ax = plt.subplots(figsize=(12, 8))
for file in src_files:
    data_array = csv_to_ndarray(src_dir + file[1])
    milliwatts = [i[0] * i[1] for i in zip(data_array[:, 1], data_array[:, 1])]
    millijoules = [np.trapz(milliwatts[:i], data_array[:i, 0]) for i, d in enumerate(milliwatts)]
    ax.plot(data_array[:, 0], millijoules, label=file[0]
            )  # Plot some data on the axes.

ax.set_xlabel('Time (seconds)')  # Add an x-label to the axes.
ax.set_title("Energy vs. Time")
ax.set_ylabel('Energy (millijoules)')  # Add a y-label to the axes.
ax.set_ybound(0, 200)
ax.set_xbound(0, 96.0)
ax.set_xticks(np.arange(0, 96 + 1, 4.0))  # setting the ticks
ax.legend()

plt.savefig(dest_graph_dir + "Energy vs. Time Combined" + ".png")

    # plt.show()

